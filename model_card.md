# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**  
I compared both models.

**Intended purpose:**  
The goal of this project is to classify short text messages or social media style posts as **positive**, **negative**, **neutral**, or **mixed**.

**How it works (brief):**  
The rule based version uses hand written rules. It preprocesses text, splits it into tokens, checks for positive and negative words, handles simple negation like `not happy` and `not bad`, gives a few words extra weight, and also checks some emoji signals.  
The ML version uses `CountVectorizer` to turn text into bag of words features and then trains a `LogisticRegression` classifier on the labeled examples in `dataset.py`.

## 2. Data

**Dataset description:**  
The final dataset contains **16 labeled posts**. The starter dataset had 6 posts, and I added 10 more. The added examples include slang, emojis, sarcasm, neutral language, and mixed feelings.

**Labeling process:**  
I labeled each post based on the overall mood of the sentence, not just one word. For example, if a sentence had both a positive and negative feeling, I labeled it as `mixed`. Some examples were easy to label, like `Today was a terrible day`. Others were harder, like sarcastic examples such as `I love getting stuck in traffic` and `Wow great, another homework packet`, because the words look positive on the surface but the meaning is negative.

**Important characteristics of your dataset:**  
- Contains slang such as `lowkey`, `no cap`, and `fire`
- Contains emojis such as `:)` and `😂`
- Includes sarcasm
- Includes mixed feeling examples like being proud but also nervous
- Includes short and ambiguous text like `This is fine` and `meh, just another day`

**Possible issues with the dataset:**  
The dataset is very small, so it does not represent real language very well. Some labels are subjective, especially sarcasm and subtle tone. The dataset also only covers a small amount of slang, emoji use, and writing styles.

## 3. How the Rule Based Model Works

**Your scoring rules:**  
I used these main rules:

- Positive words add to the score
- Negative words subtract from the score
- Some words have stronger weights, like `love`, `awesome`, `terrible`, and `exhausted`
- Some emoji and emoticons count as mood signals, like `:)`, `🙂`, `😂`, and `💀`
- Simple negation is handled by flipping the next mood word, so `not happy` becomes negative and `not bad` becomes positive
- If the sentence has both positive and negative evidence, the label becomes `mixed`
- If there is no mood evidence, the label becomes `neutral`

**Strengths of this approach:**  
The rule based model behaves predictably and is easy to explain. It works well on clear examples such as `Today was a terrible day`, `Not bad at all :)`, and `I am not happy about this`. It is also easy to debug because I can see exactly which tokens affected the score.

**Weaknesses of this approach:**  
It fails when the meaning depends on context instead of keywords. It especially struggles with sarcasm. For example, `I love getting stuck in traffic` was predicted as **positive** because the model saw `love`, even though the true label is **negative**. `Wow great, another homework packet` had the same problem.

## 4. How the ML Model Works

**Features used:**  
The ML version uses a **bag of words** representation through `CountVectorizer`.

**Training data:**  
The model was trained on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**  
After expanding the dataset, the ML model got **1.00 accuracy** on the same dataset it trained on. That looks very good, but it is only training accuracy, not a real test of generalization.

**Strengths and weaknesses:**  
A strength of the ML model is that it can learn patterns from labeled examples without me writing every rule by hand. For example, it correctly labeled the sarcastic training examples as negative.  
A weakness is that it can overfit the tiny dataset. On new examples, it still makes strange guesses. For example, it predicted `I am fine 🙂` as **negative**, and it predicted `I am not bad today` as **negative**, which shows that it is highly sensitive to the specific examples and labels it saw.

## 5. Evaluation

**How you evaluated the model:**  
I ran both models on the labeled posts in `dataset.py`.

- Rule based accuracy on the dataset: **0.88**
- ML model accuracy on the same dataset: **1.00**

The ML model’s score is misleading because it was evaluated on the same data it trained on.

**Examples of correct predictions:**  
- `Today was a terrible day` → correctly predicted as `negative` because `terrible` is a strong negative signal.
- `Not bad at all :)` → correctly predicted as `positive` because negation flipped `bad`, and `:)` added positive evidence.
- `I am proud but still nervous` → correctly predicted as `mixed` because it contains both positive and negative mood words.

**Examples of incorrect predictions:**  
- Rule based: `I love getting stuck in traffic` → predicted `positive`, but true label is `negative`. The model relied on `love` and missed sarcasm.
- Rule based: `Wow great, another homework packet` → predicted `positive`, but true label is `negative`. Again, the model treated `great` literally.
- ML on new examples: `I am fine 🙂` → predicted `negative`, which shows the model did not learn emoji context reliably from such a tiny dataset.

## 6. Limitations

The most important limitations are:

- The dataset is too small
- The ML model is evaluated on training data, not a separate test set
- The rule based model cannot understand sarcasm or deeper context reliably
- Both models depend heavily on the exact wording in the dataset
- Slang meanings can change depending on culture, age, or context
- Mixed emotions are hard to label consistently

## 7. Ethical Considerations

Mood detection can be risky in real applications. A model like this could misread a serious message, especially if someone is masking distress with humor, sarcasm, or slang. It may also misinterpret language used by different communities, age groups, or cultures. If applied to private messages, there are privacy concerns because people may not want their emotional tone analyzed automatically.

## 8. Ideas for Improvement

- Add much more labeled data
- Build a separate training set and test set
- Add better preprocessing for slang, emojis, and repeated letters
- Improve sarcasm handling, even if it is still imperfect
- Use TF-IDF instead of plain bag of words
- Test a small neural network or transformer model
- Expand the rule based vocabulary and phrase handling
- Add confidence scores instead of only hard labels
