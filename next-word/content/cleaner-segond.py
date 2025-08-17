TO_REMOVE = [
    "0","1","2","3","4","5","6","7","8","9",
    "Chapter", "¶"
]

with open("segond_1910.txt", "r") as f:
    text = f.read()
    with open("segond-clean.txt", "w") as g:
        for elem in TO_REMOVE:
            text = text.replace(elem, '')
        g.write(text)

        
