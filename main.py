from flask import Flask, render_template,request
app = Flask(__name__,template_folder="htmlpages")

todolist=[]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add',methods=['post'])
def add():
    formData=request.form
    todo=formData.get('todo')
    des=formData.get('des')

    todoDict={
        "todo":todo,
        "des":des
    }

    todolist.append(todoDict)
    return render_template('index.html',todo=todolist)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 