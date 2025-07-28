with open("kjv.txt", "r") as f:
    with open("kjv-cleaned.txt", "w") as g:
        for line in f:
            chunks = [splits for splits in line.split("\t") if splits]
            if len(chunks) == 2:
                g.write(chunks[1])
            else:
                print(f"Excluded chunk: {chunks}")

        
