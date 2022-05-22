import openai
import umap
import json
import matplotlib.pyplot as plt
import numpy as np
import os.path

openai.api_key = "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" #given by OpenAI

courses = ['18.01', '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
labels = {'18.01':'r.', '18.02':'g.', '18.03':'b.', '18.05':'mx', '18.06':'k+', '6.042':'cx', 'COMS3251':'y+'}

def make_embeddings(questions_per_course=20):
    """
    Takes json files of questions, embeds them using OpenAI's Babbage embedding engine,
    and saves a new json, embeddings.json, of the embeddings.
    """
    list_of_embeddings = []
    for course in courses:
        print("Currently embedding: " + course)
        for num in [i for i in range(1, questions_per_course+1)]:
            with open(f'./Data/{course}/{course}_Question_{num}.json', 'r') as f:
                data = json.load(f)
            raw_question = data['Original question']
            output = openai.Embedding.create(input = raw_question, engine = f'text-similarity-babbage-001')
            embedding = output['data'][0]['embedding']
            list_of_embeddings.append(embedding)
    embeddings = {'list_of_embeddings':list_of_embeddings}
    location = 'embeddings.json'
    with open(location, 'w') as f:
        f.write(json.dumps(embeddings))
    return location

def get_embeddings(embeddings_file):
    """
    Retrieves embeddings from embeddings.json 
    """
    with open(embeddings_file, 'r') as f:
        points = json.load(f)['list_of_embeddings']  #140x2048
    return np.array(points)

def reduce_via_umap(embeddings, num_dims=2):
    """
    reduces the dimensionality of points via UMAP.
    """
    reducer = umap.UMAP(n_components=num_dims)
    reduced = reducer.fit_transform(embeddings) #500x2
    return reduced

def plot_clusters(points, questions_per_course=20):
    """
    plots clusters of points.
    """
    vis_dims = points
    x = [x for x,y in vis_dims]
    y = [y for x,y in vis_dims]
    print(f'points to graph:{len(x)}')
    plt.subplots_adjust(right=0.72)
    figure = plt.gcf()
    figure.set_size_inches(9.5,6.5)
    for i in range(len(courses)):
        plt.scatter(x[i*questions_per_course:(i+1)*questions_per_course], y[i*questions_per_course:(i+1)*questions_per_course], c=labels[courses[i]][0], label=courses[i], marker = labels[courses[i]][1])
    plt.legend(bbox_to_anchor=(1, 1.01))
    plt.savefig("UMAP.png", dpi=100)
    plt.show()

if not os.path.exists('embeddings.json'):
    make_embeddings()
embeddings = get_embeddings('embeddings.json')
reduced_points = reduce_via_umap(embeddings)
plot_clusters(reduced_points)