class ORFTranslate:
    def __init__(self, dna_1):
        table = """TTT F      CTT L      ATT I      GTT V
        TTC F      CTC L      ATC I      GTC V
        TTA L      CTA L      ATA I      GTA V
        TTG L      CTG L      ATG M      GTG V
        TCT S      CCT P      ACT T      GCT A
        TCC S      CCC P      ACC T      GCC A
        TCA S      CCA P      ACA T      GCA A
        TCG S      CCG P      ACG T      GCG A
        TAT Y      CAT H      AAT N      GAT D
        TAC Y      CAC H      AAC N      GAC D
        TAA Stop   CAA Q      AAA K      GAA E
        TAG Stop   CAG Q      AAG K      GAG E
        TGT C      CGT R      AGT S      GGT G
        TGC C      CGC R      AGC S      GGC G
        TGA Stop   CGA R      AGA R      GGA G
        TGG W      CGG R      AGG R      GGG G"""
        self._table = dict(zip(table.split()[::2], table.split()[1::2]))
        self._dna_1 = dna_1
        self._dna_2 = self._reverse_complement_()
        self._translate_results = []
        self._ort_()

    def _reverse_complement_(self):
        temp = ""
        basepair = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        for c in self._dna_1:
            temp = basepair[c] + temp
        return temp

    def _translate_(self, dna):
        temp = ''
        begin = False
        end = False
        for i in range(0, len(dna), 3):
            codon = dna[i:i + 3]
            if codon == 'ATG':
                begin = True
            if begin:
                if self._table[codon] == 'Stop':
                    end = True
                    break
                temp += self._table[dna[i:i + 3]]
        if not end:
            return
        return temp

    def _ort_(self):
        self._translate_results.append(self._translate_(self._dna_1[0:]))
        self._translate_results.append(self._translate_(self._dna_1[1:]))
        self._translate_results.append(self._translate_(self._dna_1[2:]))
        self._translate_results.append(self._translate_(self._dna_2[0:]))
        self._translate_results.append(self._translate_(self._dna_2[1:]))
        self._translate_results.append(self._translate_(self._dna_2[2:]))
        for result in self._translate_results:
            if result is not None:
                for pos in range(len(result)):
                    if result[pos] == 'M' and pos != 0:
                        self._translate_results.append(result[pos:])
        self._translate_results = list(filter(None, set(self._translate_results)))
        # self._translate_results = [t for t in set(self._translate_results) if t]


if __name__ == '__main__':
    DNA = "AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG"
    test = ORFTranslate(DNA)
    pass
