from nltk.translate.bleu_score import sentence_bleu

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

trelent_bleu = 0
codex_bleu = 0
for i in range(len(references)):
    trelent_score = sentence_bleu([references[i]], trelent_hypotheses[i])
    codex_score = sentence_bleu([references[i]], codex_hypotheses[i])
    if(trelent_score != 0 or codex_score != 0):
        print(trelent_score, codex_score)
        trelent_bleu += trelent_score
        codex_bleu += codex_score

print("Trelent BLEU: ", trelent_bleu / len(references))
print("Codex BLEU: ", codex_bleu / len(references))