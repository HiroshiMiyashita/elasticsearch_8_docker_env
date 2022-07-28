import sys

def main():
    sudachi_synonym_dict_fn: str = sys.argv[1]
    elasticsearch_synonym_dict_fn: str = sys.argv[2]
    output_predicate: bool = bool(sys.argv[3])

    grpidToSynonymInfo = {}
    with open(sudachi_synonym_dict_fn, 'r') as in_f:
        for line in in_f:
            line = line.strip()
            if line == "":
                continue
            entry = line.split(",")[0:9]
            grp_id: str = entry[0]
            taigen_yougen_flag: str = entry[1]
            synonym_expand_flag: str = entry[2]
            word: str = entry[8]

            if synonym_expand_flag == "2":
                continue
            if not output_predicate and taigen_yougen_flag == "2":
                continue

            group = grpidToSynonymInfo.setdefault(grp_id, [[], []])
            if synonym_expand_flag == "0":
                group[0].append(word)
            group[1].append(word)

    with open(elasticsearch_synonym_dict_fn, 'w') as out_f:
        for _, synonymInfo in sorted(grpidToSynonymInfo.items()):
            orgWords, synonymWords = synonymInfo
            out_f.write(f'{",".join(orgWords)} => {",".join(synonymWords)}\n')


if __name__ == "__main__":
    main() 