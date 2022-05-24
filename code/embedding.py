import openai
import umap
import json
import matplotlib.pyplot as plt
import numpy as np
import os.path

openai.api_key = "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" #given by OpenAI

courses = ['18.01', '18.02', '18.03', '6.042', '18.05', '18.06', 'COMS3251']
labels = {'18.01':'r.', '18.02':'g.', '18.03':'b.', '18.05':'mx', '18.06':'k+', '6.042':'cx', 'COMS3251':'y+'}
embeddings_location = 'code/embeddings.json'

def make_embeddings(questions_per_course=20, embedding_engine = 'text-similarity-babbage-001'):
    """
    Takes json files of questions, embeds them using OpenAI's Babbage embedding engine,
    and saves a new json, embeddings.json, of the embeddings.
    """
    list_of_embeddings = []
    for course in courses:
        print("Currently embedding: " + course)
        for num in [i for i in range(1, questions_per_course + 1)]:
            if num < 10:
                number = '0' + str(num)
            else:
                number = str(num)
            with open('./Data/'+course+'/'+course+'_Question_'+number+'.json', 'r') as f:
                data = json.load(f)
            raw_question = data['Original question']
            output = openai.Embedding.create(input = raw_question, engine = embedding_engine)
            embedding = output['data'][0]['embedding']
            list_of_embeddings.append(embedding)
    embeddings = {'list_of_embeddings':list_of_embeddings}
    # location = 'code/embeddings.json'
    with open(embeddings_location, 'w') as f:
        f.write(json.dumps(embeddings))
    return None

def get_embeddings(embeddings_file):
    """
    Retrieves embeddings from embeddings_file 
    """
    with open(embeddings_file, 'r') as f:
        points = json.load(f)['list_of_embeddings']  #140x2048
    return np.array(points)

def reduce_via_umap(embeddings, num_dims=2):
    """
    reduces the dimensionality of the provided embeddings to num_dims via UMAP.
    if embeddings was an n by d np.array, it will be reduced to a n by num_dims np.array
    """
    reducer = umap.UMAP(n_components=num_dims)
    reduced = reducer.fit_transform(embeddings) #140x2
    return reduced

def plot_clusters(points, questions_per_course=20, question_labels=False, show=False, dpi=200):
    """
    plots clusters of points.
    Set question_labels to True if you want to see each point labeled with its question number.
    Set show to True if you want the created plot to pop up.
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
        if question_labels:
            for j in range(questions_per_course):
                plt.annotate(j+1, (x[questions_per_course*i+j],y[questions_per_course*i+j]), fontsize='xx-small')
    plt.legend(bbox_to_anchor=(1, 1.01))
    plt.savefig("UMAP.png", dpi=dpi)
    if show:
        plt.show()

if __name__ == "__main__":
    if not os.path.exists(embeddings_location):
        make_embeddings()
    embeddings = get_embeddings(embeddings_location)
    reduced_points = reduce_via_umap(embeddings)
    plot_clusters(reduced_points, question_labels=True)