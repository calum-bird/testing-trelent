from nltk.translate.bleu_score import sentence_bleu
import statistics

with open('data/references.txt') as f:
    data = f.read().split("====SPLIT====")

references = [
    ref.split() for ref in data
]

with open('data/codex.txt') as f:
    codex_hypothesis = f.read().split("====SPLIT====")

codex_hypotheses = [
    hyp.split() for hyp in codex_hypothesis
]

with open('data/trelent.txt') as f:
    trelent_hypothesis = f.read().split("====SPLIT====")

trelent_hypotheses = [
    hyp.split() for hyp in trelent_hypothesis
]

min_len = min(len(trelent_hypotheses), len(codex_hypotheses), len(references))

trelent_bleu = 0
codex_bleu = 0
trelent_scores = []
codex_scores = []
for i in range(min_len):
    trelent_score = sentence_bleu([references[i]], trelent_hypotheses[i])
    codex_score = sentence_bleu([references[i]], codex_hypotheses[i])
    if(trelent_score != 0 or codex_score != 0):
        trelent_bleu += trelent_score
        codex_bleu += codex_score
        trelent_scores.append(trelent_score)
        codex_scores.append(codex_score)
        #print(i)

print("Trelent avg: ", trelent_bleu / len(references))
print("Trelent median: ", statistics.median(trelent_scores))
print("Trelent best: ", max(trelent_scores))
print("Trelent worst: ", min(trelent_scores))
print("Codex avg: ", codex_bleu / len(references))
print("Codex median: ", statistics.median(codex_scores))
print("Codex best: ", max(codex_scores))
print("Codex worst: ", min(codex_scores))

