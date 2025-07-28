from importlib.metadata import version

import tiktoken
print("tiktoken version:", version("tiktoken"))

import torch
print("PyTorch version:", torch.__version__)
from torch.utils.data import Dataset, DataLoader

#========================================= analyze_sample_file
def analyze_sample_file():
    with open("the-verdict.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
        print("Total number of character:", len(raw_text))
        print(raw_text[:99])

        
#========================================= first_usage_of_tokenizer
def first_usage_of_tokenizer():
    tokenizer = tiktoken.get_encoding("gpt2")
    text = (
        "Hello, do you like tea? <|endoftext|> In the sunlit terraces"
        "of someunknownPlace."
    )
    integers = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
    print(integers)
    

#========================================= second_usage_of_tokenizer
def second_usage_of_tokenizer():
    tokenizer = tiktoken.get_encoding("gpt2")
    raw_text = ""
    with open("the-verdict.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
    enc_text = tokenizer.encode(raw_text)
    print(len(enc_text))
    print(enc_text)
    
    # taking the 50 first tokens
    sample_size = 50 
    enc_sample = enc_text[:sample_size]
    print(f"======\nSample of length {sample_size}")
    print(enc_sample)

    # determining the size of the attention window
    context_size = 4
    x = enc_sample[:context_size]
    offset = 1

    # the next tokens are 
    y = enc_sample[offset:context_size+offset]
    print(f"Taking a window of {context_size} tokens")
    print(f"x: {x}")
    print(f"With an offset of {offset} token(s)")
    print(f"y:      {y}")

    for i in range(1, context_size+1):
        context = enc_sample[:i]
        desired = enc_sample[i]
        print(context, "---->", desired)
        print(tokenizer.decode(context), "---->", tokenizer.decode([desired]))


#========================================= GPTDatasetV1
class GPTDatasetV1(Dataset):
    '''
    This class create arrays of tensors for the input and the output
    The chunks have max_length length, and the stide can create overlapping
    '''
    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_ids = []
        self.target_ids = []
        # all the text is tokenized
        token_ids = tokenizer.encode(txt)
        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i:i + max_length]
            target_chunk = token_ids[i + 1: i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]

#========================================= create_dataloader
def create_dataloader_v1(txt, batch_size=4, max_length=256, stride=128, shuffle=True, drop_last=True, num_workers=0):
    '''
    This dataloader leverages the GPTDataset
    '''
    tokenizer = tiktoken.get_encoding("gpt2")
    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers
    )
    return dataloader


#========================================= test_dataloader
def test_dataloader():
    raw_text = ""
    with open("the-verdict.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
    dataloader = create_dataloader_v1( raw_text, batch_size=1, max_length=4, stride=1, shuffle=False)
    data_iter = iter(dataloader)
    first_batch = next(data_iter)
    print(first_batch)
    second_batch = next(data_iter)
    print(second_batch)


def get_rawtext():
    with open("the-verdict.txt", "r", encoding="utf-8") as f:
        return f.read()
    
#========================================= second_test_dataloader
def secondtest_dataloader():
    raw_text = ""
    with open("the-verdict.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
    dataloader = create_dataloader_v1( raw_text, batch_size=8, max_length=4, stride=4, shuffle=False)
    data_iter = iter(dataloader)
    first_batch = next(data_iter)
    print(first_batch)

    
#========================================= embeddings_take1
def embeddings_take1():
    vocab_size = 6 # 50257 in GPT-3
    output_dim = 3 # 12288 in GPT-3
    # we generate a random matrix of 3 dimension vectors,
    #each of one being associated to a token by its index
    torch.manual_seed(123)
    embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
    # creates a tensor with vocab_size lines (on per word) and output_dim columns
    print(embedding_layer.weight)
    print(embedding_layer(torch.tensor([3])))
    input_ids = torch.tensor([2, 3, 5, 1])
    print(embedding_layer(input_ids))

    
#========================================= embeddings_take2
def embeddings_take2():
    # with bigger dimensons
    vocab_size = 50257 # 50257 in GPT-3
    output_dim = 256 # 12288 in GPT-3
    # Step 1 token embeddings
    torch.manual_seed(123)
    embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
    max_length = 4
    dataloader = create_dataloader_v1(
        get_rawtext(),
        batch_size=8,
        max_length= max_length,
        stride= max_length,
        shuffle=False)
    data_iter = iter(dataloader)
    inputs, targets = next(data_iter)
    print("Token IDs:\n", inputs)
    print("\nInputs shape:\n", inputs.shape)
    embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
    token_embeddings = embedding_layer(inputs)
    print("Tensor of the first input embedding")
    print(token_embeddings.shape)
    # Step 2 positional embeddings
    context_length = max_length
    pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)
    pos_embeddings = pos_embedding_layer(torch.arange(context_length))
    print(torch.arange(context_length))
    print(pos_embeddings.shape)
    '''
    Un embedding layer est l'association à n'importe quel élément d'une stucture de données,
    d'un vecteur de taille output_dim.
    Dans le premier cas, notre data loader nous ramène des batchs de 8 x vecteurs de 4 tokens,
    ce qui donne 8 x 4 x 256.
    Dans le second cas, context_length = 4, torch.arange(context_length) = tensor([0, 1, 2, 3])
    ce qui donne 4 x 256 une fois l'embedding passé.
    '''
    #torch.Size([8, 4, 256]) = torch.Size([8, 4, 256]) + torch.Size([4, 256])
    input_embeddings = token_embeddings + pos_embeddings
    print(input_embeddings.shape)


def softmax_naive(x):
    return torch.exp(x) / torch.exp(x).sum(dim=0)
    

#========================================= attention_take1
def attention_take1():
    # Input sentence was already embedded
    inputs = torch.tensor(
        [[0.43, 0.15, 0.89], # Your
         [0.55, 0.87, 0.66], # journey
         [0.57, 0.85, 0.64], # starts
         [0.22, 0.58, 0.33], # with
         [0.77, 0.25, 0.10], # one
         [0.05, 0.80, 0.55]] # step
    )
    print(inputs.shape) # torch.Size([6, 3])
    print(inputs.shape[0]) # 6
    all_attention_scores = torch.empty(6, 6)
    row = 0
    for input in inputs:
        print(f"---\nInput for row #{row}:", str(input))
        query = input
        # instanciation d'un vecteur de taille 6 pour
        # stocker les 6 dot product de la query embedding avec les éléments
        # de l'embedding
        attention_score = torch.empty(inputs.shape[0])
        for i, x_i in enumerate(inputs):
            attention_score[i] = torch.dot(x_i, query)
        print("1. Attention score for input (raw): " + str(attention_score))
        attention_score_normalized = attention_score / attention_score.sum()
        print("2. Attention weights (sum):", attention_score_normalized)
        print("Sum:", attention_score_normalized.sum())
        attention_score_naive = softmax_naive(attention_score)
        print("3.. Attention weights (softmax naive):", attention_score_naive)
        print("Sum:", attention_score_naive.sum())
        attention_score_sm = torch.softmax(attention_score,dim=0)
        print("3.. Attention weights (softmax Torch):", attention_score_sm)
        print("Sum:", attention_score_sm.sum())
        all_attention_scores[row] = attention_score_sm
        # le contect vector est le barycentre des embeddings
        context_vec = torch.zeros(query.shape)
        print("Context vector initialized: ",context_vec)
        for i,x_i in enumerate(inputs):
            context_vec += attention_score_sm[i]*x_i
        print("Context vector barycenter: ",context_vec)
        row +=1
    print(all_attention_scores)
    # matrix multiplication
    all_context_vecs = all_attention_scores @ inputs
    print(all_context_vecs)

    
#========================================= attention_take2
def attention_take2():
    return

        

#+++++++++++++++++++++++++++++++++++++++++++++ main
def main():
    print("****************************************analyze_sample_file*****************")
    analyze_sample_file()
    print("****************************************first_usage_of_tokenizer*****************")
    first_usage_of_tokenizer()
    print("****************************************second_usage_of_tokenizer*****************")
    second_usage_of_tokenizer()
    print("****************************************test_dataloader*****************")
    test_dataloader()
    print("****************************************secondtest_dataloader*****************")
    secondtest_dataloader()
    print("****************************************embeddings_take1*****************")
    embeddings_take1()
    print("****************************************embeddings_take2*****************")
    embeddings_take2()
    print("****************************************attention_take1*****************")
    attention_take1()
    
if __name__ == "__main__":
    main()
