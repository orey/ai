from unstructured.partition.auto import partition

elements = partition("AttentionIsAllYouNeed.pdf")

print("\n\n".join([str(el) for el in elements]))
