import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Create knowledge base: 100 sentences on various topics
knowledge_base = [
    "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
    "Photosynthesis is the process by which green plants use sunlight to synthesize foods.",
    "Machine learning algorithms can be supervised, unsupervised, or semi-supervised.",
    "A balanced diet includes fruits, vegetables, whole grains, and lean proteins.",
    "The Great Wall of China is over 13,000 miles long.",
    "Python is a high-level, interpreted programming language known for its readability.",
    "Deep learning models use neural networks with many layers to learn complex patterns.",
    "Yoga is an ancient practice that combines physical postures, breathing exercises, and meditation.",
    "The theory of relativity was developed by Albert Einstein.",
    "To make a healthy smoothie, blend spinach, banana, and almond milk.",
    "Support vector machines are effective in high-dimensional spaces.",
    "The Amazon rainforest produces more than 20% of the world's oxygen.",
    "Regular exercise reduces the risk of chronic diseases.",
    "JavaScript is a versatile language used for both front-end and back-end development.",
    "Natural language processing enables computers to understand human language.",
    "Quinoa is a gluten-free grain rich in protein and fiber.",
    "The Louvre Museum in Paris houses the Mona Lisa.",
    "Blockchain technology provides a decentralized and secure ledger.",
    "Grilled salmon with steamed vegetables is a heart-healthy meal.",
    "Reinforcement learning is a type of machine learning where an agent learns by interacting with an environment.",
    "Shakespeare wrote many famous tragedies including Hamlet and Macbeth.",
    "The human brain contains approximately 86 billion neurons.",
    "A Mediterranean diet emphasizes olive oil, fish, and fresh produce.",
    "Cloud computing allows on-demand access to computing resources over the internet.",
    "K-nearest neighbors is a simple, non-parametric classification algorithm.",
    "The Industrial Revolution began in Britain in the late 18th century.",
    "Spinach is packed with iron and vitamins A and C.",
    "Data visualization helps in understanding patterns and trends in data.",
    "Mount Everest is the tallest mountain in the world.",
    "Convolutional neural networks are especially good at image recognition tasks.",
    "Hydration is essential for maintaining body temperature and joint health.",
    "The internet has revolutionized the way we communicate and access information.",
    "Decision trees are intuitive models that split data based on feature values.",
    "The Renaissance was a period of great cultural and scientific rebirth in Europe.",
    "Avocado is a nutrient-dense fruit that contains healthy monounsaturated fats.",
    "SQL is a standard language for managing relational databases.",
    "Random forests combine multiple decision trees to improve accuracy.",
    "Beethoven composed symphonies that remain influential today.",
    "Intermittent fasting involves cycling between periods of eating and fasting.",
    "Linear regression models the relationship between a dependent variable and one or more independent variables.",
    "The Pacific Ocean is the largest and deepest ocean on Earth.",
    "Artificial intelligence aims to create systems that can perform tasks requiring human intelligence.",
    "Oatmeal topped with berries and nuts makes a filling, nutritious breakfast.",
    "API stands for Application Programming Interface.",
    "Gradient boosting is a powerful ensemble technique often used in competitions.",
    "The printing press, invented by Gutenberg, revolutionized the spread of information.",
    "Chia seeds are an excellent source of omega-3 fatty acids and fiber.",
    "Version control systems like Git help teams collaborate on code.",
    "Principal component analysis reduces the dimensionality of data while preserving variance.",
    "The Pyramids of Giza are among the Seven Wonders of the Ancient World.",
    "Whole grain bread is healthier than white bread because it retains the bran and germ.",
    "Cybersecurity involves protecting systems from digital attacks.",
    "Naive Bayes classifiers are based on applying Bayes' theorem with strong independence assumptions.",
    "The human body contains 206 bones.",
    "Turmeric contains curcumin, which has anti-inflammatory properties.",
    "Data mining is the process of discovering patterns in large data sets.",
    "The solar system consists of the sun and everything that orbits it.",
    "Recurrent neural networks are designed to handle sequential data.",
    "Eating a high-fiber diet can help lower cholesterol levels.",
    "Agile is an iterative approach to software development.",
    "Time series forecasting uses historical data to predict future values.",
    "The Roman Empire was one of the largest empires in ancient history.",
    "Kale is a leafy green vegetable packed with vitamins K, A, and C.",
    "Docker enables developers to package applications into containers.",
    "Feature engineering is crucial for improving model performance.",
    "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
    "Probiotics are beneficial bacteria that support gut health.",
    "Neural style transfer uses deep learning to combine the content of one image with the style of another.",
    "The French Revolution began in 1789.",
    "Sweet potatoes are a great source of beta-carotene and complex carbohydrates.",
    "Big data technologies like Hadoop and Spark process massive datasets.",
    "Clustering algorithms group similar data points together without labeled outputs.",
    "The Sahara Desert is the largest hot desert in the world.",
    "Resistance training helps build muscle strength and bone density.",
    "Chatbots use NLP to simulate conversation with users.",
    "Water boils at 100 degrees Celsius at sea level.",
    "Bananas are rich in potassium, which helps regulate blood pressure.",
    "Overfitting occurs when a model learns noise instead of the underlying pattern.",
    "The Wright brothers made the first powered flight in 1903.",
    "Mindfulness meditation can reduce stress and improve focus.",
    "A RESTful API uses HTTP requests to GET, PUT, POST and DELETE data.",
    "Ensemble methods combine multiple models to boost predictive performance.",
    "The Mona Lisa was painted by Leonardo da Vinci in the early 1500s.",
    "Tofu is a versatile plant-based protein made from soybeans.",
    "Unsupervised learning finds hidden patterns in unlabeled data.",
    "The Northern Lights are caused by solar particles interacting with the Earth's magnetic field.",
    "Blueberries are high in antioxidants and may improve memory.",
    "Transfer learning leverages a pre-trained model on a new, similar problem.",
    "The Nile River is the longest river in the world.",
    "Cooking with olive oil instead of butter can reduce saturated fat intake.",
    "Natural language generation is used to produce text from structured data.",
    "The Statue of Liberty was a gift from France to the United States.",
    "Lentils are a great source of plant-based protein and iron.",
    "Cross-validation is a technique for assessing how a model will generalize to an independent dataset.",
    "The Earth revolves around the Sun once every 365.25 days.",
    "Hummus, made from chickpeas, is a healthy dip rich in fiber.",
    "Hyperparameter tuning improves model accuracy by finding optimal settings."
]

# 2. Load a pre-trained sentence embedding model (lightweight, good quality)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode all sentences
sentence_embeddings = model.encode(knowledge_base)

# 3. Search function: embed query, compute cosine similarity, return top K
def search(query, top_k=5):
    query_embedding = model.encode([query])[0]
    # Cosine similarity between query and all sentence embeddings
    similarities = cosine_similarity([query_embedding], sentence_embeddings)[0]
    # Get indices of top_k results (highest similarity)
    top_indices = np.argsort(similarities)[::-1][:top_k]
    results = []
    for idx in top_indices:
        results.append({
            'sentence': knowledge_base[idx],
            'score': round(float(similarities[idx]), 4)
        })
    return results

# 4. Test queries
print("Query: 'machine learning algorithms'")
for res in search("machine learning algorithms", top_k=5):
    print(f"Score: {res['score']:.4f} | {res['sentence']}")

print("\nQuery: 'healthy food recipes'")
for res in search("healthy food recipes", top_k=5):
    print(f"Score: {res['score']:.4f} | {res['sentence']}")