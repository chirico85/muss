# from https://github.com/facebookresearch/fairseq/issues/2120#issuecomment-661622230
import argparse
from glob import glob

from fairseq.data import Dictionary
from fairseq.tokenizer import tokenize_line

def pad_dict(d: Dictionary, num_extra_symbols: int, padding_factor: int = 8) -> None:
    i = 0
    while (len(d) + num_extra_symbols) % padding_factor != 0:
        symbol = f"madeupword{i:04d}"
        d.add_symbol(symbol, n=0)
        i += 1

def main() -> None:
    parser = argparse.ArgumentParser(description="Build vocabulary from corpus data.")
    parser.add_argument("--corpus-data", type=str, required=True, help="The path pattern (glob) to all tokenized corpus files (train, test, val).")
    parser.add_argument("--langs", type=str, required=True, help="The pre-trained model languages.")
    parser.add_argument("--output", type=str, required=True, help="The vocabulary file.")
    args = parser.parse_args()

    langs = args.langs.split(",")
    ft_dict = Dictionary()
    for data_path in glob(args.corpus_data):
        Dictionary.add_file_to_dictionary(data_path, ft_dict, tokenize_line, 4)
    ft_dict.finalize(padding_factor=0)
    pad_dict(ft_dict, len(langs) + 1)
    ft_dict.save(args.output)

if __name__ == "__main__":
    main()