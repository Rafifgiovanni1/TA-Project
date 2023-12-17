from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB,CategoricalNB
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class Process:
    confusion_matrix = None
    score = None
    classification_score = None

    dataset = pd.read_csv("dataset_Terbalik.csv")

    def __init__(self,data: pd.DataFrame):
        self.data = data

    def process(self):
        self.dataset = self.dataset.drop(["name","major"],axis=1)
        
        encoder = LabelEncoder()
        
        self.dataset["activity"] = encoder.fit_transform(self.dataset["activity"])
        self.dataset["achievement"] = encoder.fit_transform(self.dataset["achievement"])
        self.dataset["nonacademic_achievement"] = encoder.fit_transform(self.dataset["nonacademic_achievement"])
        self.dataset["accept_status"] = encoder.fit_transform(self.dataset["accept_status"])
        
        x = self.dataset.drop(["accept_status"],axis=1)
        y = self.dataset["accept_status"]

        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=10)
        classifier = CategoricalNB()
        classifier.fit(x_train,y_train)
        y_pred = classifier.predict(x_test)
        self.score = accuracy_score(y_test,y_pred)
        self.confusion_matrix = confusion_matrix(y_pred,y_test)
        self.classification_score = classification_report(y_pred,y_test,output_dict=True)

        self.data["activity"] = encoder.fit_transform(self.data["activity"])
        self.data["achievement"] = encoder.fit_transform(self.data["achievement"])
        self.data["nonacademic_achievement"] = encoder.fit_transform(self.data["nonacademic_achievement"])        
        
        def processing(data):           
            result = classifier.predict([[data["score"],data["activity"],data["achievement"],data["nonacademic_achievement"]]])
            return result[0]

        self.data["accept_status"] = self.data.apply(processing,axis=1)
        self.data["accept_status"] = encoder.inverse_transform(self.data["accept_status"])
        self.data["activity"] = encoder.inverse_transform(self.data["activity"])
        self.data["achievement"] = encoder.inverse_transform(self.data["achievement"])
        self.data["nonacademic_achievement"] = encoder.inverse_transform(self.data["nonacademic_achievement"])
        print(self.confusion_matrix)



