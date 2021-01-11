import statistics

class Fasta_file:
    
    def __init__(self, path):
        self.filepath = path
        self.isfasta = self.Check_if_valid()
        self.filename = path.split('/')[-1]
        self.seqs = self.Read_to_dict()
        self.number_seqs = len(self.seqs)
        self.average_lengths, self.lengths, self.average_masked, self.masked, self.average_GC, self.GC, self.average_gaps, self.gaps = self.Get_sequence_info()
        self.max_length = max(self.lengths)
        self.min_length = min(self.lengths)

    def Check_if_valid(self):
        '''Super simple way of checking to see if the fasta appears to be valid. 
            Just checks the first character of each line for valid characters.'''
        valid_chars = ['>', 'A', 'T', 'C','G','a','t','c','g','N','n', '-', '\n'] # currently does not include all valid IUPAC characters
        with open(self.filepath, 'r') as f:
            for line in f:
                if line[0] not in valid_chars:
                    print("This does not appear to be a fasta file. A line begins with non-accepted character: ".format(str(line[0])))
                    return False
        return True


    def Read_to_dict(self):
        fasta_dict = {}
        with open(self.filepath, 'r') as f:
            for line in f:
                if line.startswith('>'):
                    header = line.strip()
                    seq = ''
                else:
                    seq += line.strip()
                    fasta_dict[header] = seq
        return fasta_dict
    

    def Get_sequence_info(self):
        '''I only want to loop through the file once ideally, so lets get as much information here as I can'''
        masked = []
        GC = []
        gaps = []
        lengths = []
        gc_chars = ["G", "C", "g", "c"]
        for value in self.seqs.values():
            seq_length = len(value)
            lengths.append(seq_length)
            masked_count = 0
            gc_count = 0
            gap_count  = 0
            for char in value:
                if char.islower():
                    masked_count += 1
                if char in gc_chars:
                    gc_count += 1
                if char == '-':
                    gap_count += 1
            masked.append(masked_count/seq_length)
            GC.append(gc_count/seq_length)
            gaps.append(gap_count/seq_length)
        average_masked = statistics.mean(masked)
        average_GC = statistics.mean(GC)
        average_gaps = statistics.mean(gaps)
        average_lengths = statistics.mean(lengths)
        return average_lengths, lengths, average_masked, masked, average_GC, GC, average_gaps, gaps
