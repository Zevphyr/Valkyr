#import the application
from app import app
# start the application if this is the main python module (which it is)
if __name__ == "__main__":
  app.run()

"""
Open a terminal window and if running on windows type:


In the terminal window, navigate to your project folder type python app.py, we should get the following output:

   * Running on http://127.0.0.1:5000/


"""