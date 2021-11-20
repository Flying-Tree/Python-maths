# Python-maths

Python scripts for maths or related fields (information theory for now).

## [factorisation_polynome_tk.py](https://github.com/Flying-Tree/Python-maths/blob/main/factorisation_polynomes_tk.py)

Polynomial factorization in the set of rational numbers, with a Tkinter GUI. If a trinomial is found, its complex roots are calculated.

## [str-encoding.py](https://github.com/Flying-Tree/Python-maths/blob/main/str-encoding.py)

Different methods to encode and decode strings into binary sequences. It is a completely theorical script so more 

### Huffman coding

#### Description

Encodes and decodes a string using Huffman coding ([Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)). This entropic coding considers only the frequences of characters, and not the set of probability for a symbol to follow another symbol.

Both the source and the destination must use the same tree, hence either they use a predefined tree either the tree is transmitted.

You can use a predefined tree and this is better for short messages with few different symbols, but you lose the adaptability of this encoding method, especially if the message contains many unusual symbols. Therefore it is better to use the automatically generated tree for long strings with many symbols.

#### Documentation

* A ```huffman``` contains the original message, the encoded message, and the tree. You can set some these variables using ```var = huffman( message = ' ... ' )``` at creation, or later ```var.message = ' ... '``` (both work with ```tree``` or ```coded``` instead of ```message```).

* ```encode``` method can be called to update the value of ```coded``` and ```tree```. Concerning ```tree```, the scripts tries to use the current value of ```tree``` but if a character is not in the tree, a new one is created with the current ```message```, without considering the former ```tree```. Moreover, nothing in the output says if the tree changed.

* ```decode``` method sets the value of ```message``` to the message associated with ```tree``` and ```coded```. It doesn't detect if ```tree``` and ```coded``` are matching (there may be useless digits at the end of ```coded```).
