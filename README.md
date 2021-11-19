# Python-maths

Python scripts for maths

## factorisation_polynome_tk.py

Polynomial factorization in the set of rational numbers, with a Tkinter GUI. If a trinomial is found, its complex roots are calculated.

## str-encoding.py

Different methods to encode and decode strings into binary sequences.

### Huffman coding

Encodes and decodes a string using Huffman coding ([Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)). This entropic coding considers only the frequences of characters, and not the set of probability for a symbol to follow another symbol.

Both the source and the destination must use the same tree, hence either they use a predefined tree either the tree is transmitted.

You can use a predefined tree in the '''\*args''' using a format similar to the tree in the output. This is better for short messages with few different symbols, but you lose the adaptability of this encoding method, especially if the message contains many unusual symbols. Therefore it is better to use the automatically generated tree for long strings with many symbols.
