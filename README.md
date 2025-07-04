# Intro
This project (**Circuit**) is about Boolean circuit and arithmetic circuit, which are widely used in computer science and cryptography, with applications including Garbled Circuits (GC) and Secret Sharing (SS).

# Run
```shell
python3 bristol_circuit.py
```
## Output
>```
> #(total gates) = 36663
> #(total wires) = 36919
> #(input variables) = 2, bit length of each vairable [128, 128]
> #(output variables) = 1, bit length of each variable [128]
> circuit input: 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
> circuit output: 01110010011001101011000101111100010010111110001011001110010111110101000001011010101000010101011110010011001100011101101011111100
>```

# Draw
Copy the content from the generated 'graph.txt' file and paste it into the website at https://dreampuf.github.io/GraphvizOnline.

# Reference

[Bristol Fashion] https://nigelsmart.github.io/MPC-Circuits

[LowMC Circuit] https://github.com/jacob14916/GigaDORAM-USENIX23-Artifact/blob/main/circuits/LowMC_File.txt

[LowMC Paper] https://eprint.iacr.org/2023/1950.pdf
>... The instantiation of LowMC
we use has 46837 total gates, out of which 1134 are ANDs,
stacked into 9-AND-depth circuit. By contrast, AES has a
total of 36663 gates, out of which 6400 are ANDs, stacked
into a 60-AND-depth-circuit ...
