from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os
import json
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')
Config.write()

Builder.load_string('''
<displayResult>:
    Label:
        text: root.text
        font_size: 15
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            path: "C:/dissertation/causcumber/scenarios/compare_interventions/features"

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)
        
''')


class displayResult(ScrollView):
    text = StringProperty('')

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class main(App):

    created_file = []
    loadfile = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(main,self).__init__(**kwargs)
        os.chdir('compare_interventions')

    def build(self):

        Window.bind(on_request_close=self.on_request_close)
        
        Layout = BoxLayout(orientation = 'vertical')
        banner = Label(text='Causcumber', size_hint=(1, 0.1))
        Layout.add_widget(banner)

        displayLayout = GridLayout(cols=2,  width="600dp")

        resultLayout = GridLayout(cols=1,  width="600dp")
        self.select_feature_file = Button(text='Select feature file', size_hint=(1, 0.1)) # Choose feature file to run
        self.select_feature_file.bind(on_press=self.show_load)
        #self.select_feature_file = selectFile()
        resultLayout.add_widget(self.select_feature_file) 
        self.Result = Label(text='Result', size_hint=(1, 0.1)) # Title
        resultLayout.add_widget(self.Result)
        self.display_result = displayResult(text='') # Display result
        resultLayout.add_widget(self.display_result)    
        displayLayout.add_widget(resultLayout) 

        inputLayout = GridLayout(cols=1,  width="600dp")
        self.choose_input_title = Label(text='Choose different input', size_hint=(1, 0.1)) # Title
        inputLayout.add_widget(self.choose_input_title) 
        self.paremeter1 = Label(text='Parameter 1', size_hint=(1, 0.1)) #modify parameter 1
        inputLayout.add_widget(self.paremeter1) 
        self.input1 = TextInput(text='', size_hint=(1, 1.0), multiline=False) 
        inputLayout.add_widget(self.input1)
        self.paremeter2 = Label(text='Parameter 2', size_hint=(1, 0.1)) #modify parameter 2
        inputLayout.add_widget(self.paremeter2) 
        self.input2 = TextInput(text='', size_hint=(1, 1.0), multiline=False) 
        inputLayout.add_widget(self.input2)   
        displayLayout.add_widget(inputLayout)

        runBehave = Button(text='Run behave', size_hint=(1, 0.1)) # Run update function 
        runBehave.bind(on_press=self.update)
        displayLayout.add_widget(runBehave) 

        saveInput = Button(text='Save input', size_hint=(1, 0.1)) # save input as new feature file
        saveInput.bind(on_press=self.save_file)
        displayLayout.add_widget(saveInput) 

        Layout.add_widget(displayLayout)

        return Layout

    def update(self, userInput):
        if os.path.isfile("results.json") == True:
            json_file = open("results.json")
            outputs = json.load(json_file)
            json_file.close()    
            # Convert json to string
            data = json.dumps(outputs)
            result = data
            split_data = data.split()
            result = ""
            word_count = 0
            for split_data in split_data:
                result += split_data + " "
                word_count += 1
                if word_count == 6 or "." in split_data:
                    result += "\n"
                    word_count = 0

            self.display_result.text = result
        else:
            self.display_result.text = "Please select a feature file"      

    def save_file(self, instance):
        parameter_input1 = self.input1.text
        parameter_input2 = self.input2.text
        feature_file_name = "compare_" + parameter_input1 + "_" + parameter_input2 + ".feature"    #generate file name based on input
        self.created_file.append(feature_file_name)
        os.chdir('features')
        f = open(feature_file_name, "a")                                                           #generate feature file with input file name
        f.write(parameter_input1 + parameter_input2)
        f.close()
        os.chdir('..')

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, instance):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        filename = filename[0].replace('C:\\dissertation\\causcumber\\scenarios\\compare_interventions\\features\\', '')
        file = open("results.json","w")
        file.close()
        print("File cleaned")
        behave_cmd = "behave features/"+ filename + " --format json --outfile results.json"
        #behave_cmd = "behave features/"+ filename + " --format json --junit"
        os.system(behave_cmd)       
        self.dismiss_popup()
    
    def on_request_close(self, instance):  #remove results.json and other feature file created when closing the program
        os.remove("results.json")
        os.chdir('features')
        for self.created_file in self.created_file:
            os.remove(self.created_file)
        os.chdir('..')
        print("Closing")

Factory.register('LoadDialog', cls=LoadDialog)
main().run()