import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Define the Streamlit app
def app():
    if "reset_app" not in st.session_state:
        st.session_state.reset_app = False

    st.title('ML Classifiers on the Iris Dataset')

    # Use session state to track the current form
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1    

    # Display the appropriate form based on the current form state
    if st.session_state["current_form"] == 1:
        display_form1()
    elif st.session_state["current_form"] == 2:
        display_form2()
    elif st.session_state["current_form"] == 3:
        display_form3()

    if "clf" not in st.session_state: 
        st.session_state["clf"] = []

    if "X_train" not in st.session_state: 
        st.session_state["X_train"] = []

    if "X_test" not in st.session_state: 
        st.session_state["X_test"] = []
    
    if "y_train" not in st.session_state: 
        st.session_state["X_train"] = []
    
    if "y_test" not in st.session_state: 
        st.session_state["y_yest"] = []

    if "selected_model" not in st.session_state: 
        st.session_state["selected_model"] = 0

def display_form1():
    st.session_state["current_form"] = 1
    form1 = st.form("intro")

    text = """Louie F. Cervantes, M. Eng. (Information Engineering) \n\n
    CCS 229 - Intelligent Systems
    Computer Science Department
    College of Information and Communications Technology
    West Visayas State University"""
    form1.text(text)

    form1.header('Description')
    form1.image('iris_flower.jpg', caption="The Iris Plant", use_column_width=True)
    text = """The iris is a beautiful and diverse flowering plant genus, 
    boasting over 310 recognized species. These plants are known for their 
    stunning blooms, which come in a wide range of colors, including purple, 
    blue, yellow, white, and even black."""
    form1.subheader('The Iris Dataset')

    form1.write(text)

    text = """The Iris dataset is a well-known and widely used dataset in the field
    of machine learning. Here's a breakdown of its key aspects:"""
    form1.write(text)
    text = """Data points: 150, representing 50 samples from each of three Iris species: 
    Iris setosa, Iris versicolor, and Iris virginica.
    \nFeatures: Four measurements for each flower (in centimeters): Sepal length, 
    Sepal width, Petal length, Petal width
    \nTarget variable: The species of the Iris flower (Setosa, Versicolor, or Virginica)."""
    form1.write(text)
    form1.write('Applications:')
    text = """Commonly used to introduce and test various machine learning algorithms, 
    especially for: Classification (predicting the flower species based on the
    measurements) Visualization (exploring relationships between features and species)"""
    form1.write(text)
  

    submit1 = form1.form_submit_button("Start")

    if submit1:
        form1 = [];
        # Go to the next form        
        display_form2()

def display_form2():
    st.session_state["current_form"] = 2

    form2 = st.form("training")
    # Load the iris dataset
    data = load_iris()

    # Convert data features to a DataFrame
    feature_names = data.feature_names
    df = pd.DataFrame(data.data, columns=feature_names)
    df['target'] = data.target
    
    form2.write('The iris dataset')
    form2.write(df)

    # Separate features and target variable
    X = df.drop('target', axis=1)  # Target variable column name
    y = df['target']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #save the values to the session state
    st.session_state['X_train'] = X_train
    st.session_state['X_test'] = X_test
    st.session_state['y_train'] = y_train
    st.session_state['y_test'] = y_test

    form2.write('Interesting characteristics:')
    text = """One species (Setosa) is easily distinguishable from the others 
    based on its sepal measurements. The other two species (Versicolor and Virginica) 
    have some overlap in their measurements, making them more challenging to 
    distinguish solely based on two features. Overall, the Iris dataset, despite its 
    simplicity, offers a valuable resource for understanding and practicing 
    fundamental machine learning concepts."""
    form2.write(text)

    form2.subheader('Browse the Dataset') 
    form2.write(df)

    form2.subheader('Dataset Description')
    form2.write(df.describe().T)

    # Create a figure and an axis
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create a scatter plot with color based on species
    sns.scatterplot(
        x="sepal width (cm)",
        y="sepal length (cm)",
        hue="target",
        palette="deep",
        data=df,
        ax=ax,
    )

    # Add labels and title
    ax.set_xlabel("Sepal Width (cm)")
    ax.set_ylabel("Sepal Length (cm)")
    ax.set_title("Sepal Width vs. Sepal Length by Iris Species")

    # Add legend
    plt.legend(title="Species")

    # Show the plot
    form2.pyplot(fig)

    text = """One species (Setosa) is easily distinguishable 
    from the others based on its sepal measurements"""
    form2.write(text)

    # Create a figure and an axis
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create a scatter plot with color based on species
    sns.scatterplot(
        x="petal width (cm)",
        y="petal length (cm)",
        hue="target",
        palette="bright",
        data=df,
        ax=ax,
    )

    # Add labels and title
    ax.set_xlabel("Petal Width (cm)")
    ax.set_ylabel("Petal Length (cm)")
    ax.set_title("Petal Width vs. Petal Length by Iris Species")

    # Add legend
    plt.legend(title="Species")

    # Show the plot
    form2.pyplot(fig)

    text = """The clusters show the distint species based on 
    their petal measurements"""
    form2.write(text)

    form2.subheader('Select the classifier')

    # Create the selecton of classifier

    clf = GaussianNB() 
    options = ['Logistic Regression', 'Naive Bayes', 'Support Vector Machine']
    selected_option = form2.selectbox('Select the classifier', options)
    if selected_option =='Logistic Regression':
        clf = LogisticRegression(C=1.0, class_weight=None, 
            dual=False, fit_intercept=True,
            intercept_scaling=1, max_iter=100, multi_class='auto',
            n_jobs=1, penalty='l2', random_state=42, solver='lbfgs',
            tol=0.0001, verbose=0, warm_start=False)
        st.session_state['selected_model'] = 0
    elif selected_option=='Support Vector Machine':
        clf = SVC(kernel='rbf', gamma=10) 
        st.session_state['selected_model'] = 2
    else:
        clf = GaussianNB()
        st.session_state['selected_model'] = 1

    # save the clf to the session variable
    st.session_state['clf'] = clf

    submit2 = form2.form_submit_button("Train")
    if submit2:     
        display_form3()

def display_form3():
    st.session_state["current_form"] = 3
    form3 = st.form("Result")
    classifier = ''
    if st.session_state['selected_model'] == 0:     # logistic regression
        text = """Logistic regression is easy to interpret. Coefficients 
        provide insights into the relationship between features 
        and class probabilities. Relatively fast training compared to 
        some other algorithms.."""
        classifier = 'Logistic Regression'
    elif st.session_state['selected_model'] == 1:   # naive bayes
        text = """Naive bayes is simple to implement and computationally 
        efficient. Performs well with independent features (features with 
        minimal correlation)."""
        classifier = 'Naive Bayes'
    else:   # SVM
        text = """SVM generally achieves the highest accuracy on the Iris dataset.
        It has good performance on various datasets, including those with 
        non-linear relationships. It can be effective for high-dimensional data."""
        classifier = "Support Vector Machine"

    form3.subheader('Performance of the ' + classifier)

    X_train = st.session_state['X_train']
    X_test = st.session_state['X_test']
    y_train= st.session_state['y_train']
    y_test = st.session_state['y_test']

    clf = st.session_state['clf']
    clf.fit(X_train, y_train)
    y_test_pred = clf.predict(X_test)

    form3.subheader('Confusion Matrix')
    form3.write('Confusion Matrix')
    cm = confusion_matrix(y_test, y_test_pred)
    form3.text(cm)

    form3.subheader('Performance Metrics')
    form3.text(classification_report(y_test, y_test_pred))

    form3.write(text)

    # save the clf to the session state
    st.session_state['clf'] = clf

    submit3 = form3.form_submit_button("Reset")
    if submit3:
        st.session_state.reset_app = True
        st.session_state.clear()
        form3.write("If the form does not reset, click the reset button again.")

if __name__ == "__main__":
    app()
