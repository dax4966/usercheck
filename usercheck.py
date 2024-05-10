import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    #print('test run for load')
    return render_template('upload.html')

@app.route('/upload', methods = ['POST','GET'])

def upload():
    if request.method == "POST" :
        print('file upload called')
        file = request.files['file']
        #file.save(file.filename)
        file.save('./Data/'+file.filename)
        print(file.filename)
        # df = pd.read_csv(file.filename)
        df = pd.read_csv('./Data/'+file.filename)
        
        print('---------------- New calculation ------------------')

        debit_sum = df.loc[df['transanctionRelatedType'].isin(['EntryFee', 'Withdrawal']) & (df['transactionStatus'].isin(['Success','Pending'])), 'amount'].sum()
        credit_sum = df.loc[df['transanctionRelatedType'].isin(['Signup Bonus', 'Credit', 'Winnings', 'Refund']) & (df['transactionStatus'] == 'Success'), 'amount'].sum()
        print('Debit Sum - :',debit_sum)
        print('Credit Sum - :',credit_sum)
        print('Difference - :',format(credit_sum - debit_sum, ".2f") )
        difference = credit_sum - debit_sum

        # Save results
        # results = pd.DataFrame({
        #     'Debit Sum': [debit_sum],
        #     'Credit Sum': [credit_sum],
        #     'Difference': [difference]
        # })

        resultObj = {
            'debit_sum': debit_sum,
            'credit_sum': credit_sum,
            'difference': difference
        }

        # results.to_csv('results.csv', index=False)

        
        return render_template('result.html', **resultObj )
    

@app.route('/result', methods = ['POST','GET'])
def result():
    print('after file called')
    

if __name__ == '__main__':
    print('triggred')
    app.run(debug=True)







