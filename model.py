import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
def data_split(data, ratio):
    #np.random.seed(42)
    shuffled = np.random.permutation(len(data))
    test_size = int(len(data) * ratio)
    test_indices = shuffled[:test_size]
    train_indices = shuffled[test_size:]
    return data.iloc[train_indices], data.iloc[test_indices]
if __name__ == "__main__":
    df=pd.read_csv("E:/Users/NM/envs/Recsys/surveybot/Madedata1.csv")
    df['Contact_with_covid_patient'] = df['Contact_with_covid_patient'].map({'No': 0, 'Yes': 2,'Not known':1})
    df['Contact_with_covid_patient'] = df['Contact_with_covid_patient'].fillna(1)
    df['Contact_with_covid_patient'] = df['Contact_with_covid_patient'].astype(int)
    train, test = data_split(df,0.1)

    X_train = train[['Age','fever','Bodypain','Runny_nose','Difficulty_in_breathing','Nasal_congestion','Sore_throat','Contact_with_covid_patient']].to_numpy()
    X_test = test[['Age','fever','Bodypain','Runny_nose','Difficulty_in_breathing','Nasal_congestion','Sore_throat','Contact_with_covid_patient']].to_numpy()

    Y_train = train[['Infected']].to_numpy().reshape(2250, )
    Y_test = test[['Infected']].to_numpy().reshape(249, )

    clf = LogisticRegression()
    clf.fit(X_train, Y_train)
   
    # open a file, where you ant to store the data
    file = open('model.pkl', 'wb')
    
    # dump information to that file
    pickle.dump(clf, file)

    # close the file
    file.close()

