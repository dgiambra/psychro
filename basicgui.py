from tkinter import Tk, Label, Button, Entry, DoubleVar, END, W, E
import math

class Psychro:
    
    def water_vapor_saturation_pressure(temp):
        temp = temp + 459.67
        if temp > 32 + 459.67:
            c8 = -1.0440397*10**4
            c9 = -1.1294650*10**1
            c10 = -2.7022355*10**-2
            c11 = 1.2890360*10**-5
            c12 = -2.4780681*10**-9
            c13 = 6.5459673*10**0
            
            pws = math.exp(c8/temp+c9+c10*temp+c11*temp**2+c12*temp**3+c13*math.log(temp))
            
        elif temp < 32 + 459.67:
            c1 = -1.0214165*10**4
            c2 = -4.8932428*10**0
            c3 = -5.3765794*10**-3
            c4 = 1.9202377*10**-7
            c5 = 3.5575832*10**-10
            c6 = -9.0344688*10**-14
            c7 = 4.1635019*10**0
            
            pws = math.exp(c1/temp+c2+c3*temp+c4*temp**2+c5*temp**3+c6*temp**4+c7*math.log(temp))
        return pws
    
    def partial_pressure_water(sat_pressure, relative_humidity):
        pw = relative_humidity*sat_pressure
        return pw

    def humidity_ratio(partial_pressure, pressure):
        W = 0.621945*partial_pressure/(pressure-partial_pressure)
        return W
        
    def get_humidity_ratio(temp, relative_humidity, pressure = 14.696):
        if relative_humidity > 1:
            relative_humidity /= 100
            # print(relative_humidity)
        sat_pressure = Psychro.water_vapor_saturation_pressure(temp)
        # print(sat_pressure)
        partial_pressure = Psychro.partial_pressure_water(sat_pressure,relative_humidity)
        # print(partial_pressure)
        humidity = Psychro.humidity_ratio(partial_pressure, pressure) * 7000
        # print(humidity)
        return humidity
        
class Calculator:
    def __init__(self,master):
        self.master = master
        master.title("Calculator")

        self.hr = 0
        self.temp = 0
        self.rh = 0
        self.total_label_text = DoubleVar()
        self.total_label_text.set(self.hr)
        self.total_label = Label(master, textvariable=self.total_label_text)
        self.label = Label(master, text='HR: ')
        self.templabel = Label(master, text = 'Temp (F):')
        self.rhlabel = Label(master, text = 'RH:')
        vcmdtemp = master.register(self.validatetemp)
        vcmdrh = master.register(self.validaterh)
        self.entrytemp = Entry(master, validate = "key", validatecommand=(vcmdtemp,'%P'))
        self.entryrh = Entry(master, validate = "key", validatecommand=(vcmdrh,'%P'))

        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=1,column = 1, columnspan=2, sticky=E)

        self.templabel.grid(row=2,column=0,sticky=W)
        self.entrytemp.grid(row=3, column=0,columnspan=3, sticky=W+E)
        
        self.rhlabel.grid(row=4, column=0, sticky=W)
        self.entryrh.grid(row=5, column=0, columnspan=3, sticky=W+E)

    def validatetemp(self, new_text):
        if not new_text:
            self.temp = 0
            return True

        try:
            if new_text == '-':
                return True
            self.temp = float(new_text)
            # print(self.A)
            self.hr = Psychro.get_humidity_ratio(self.temp, self.rh)
            # print(self.total)
            self.update()
            return True
        except ValueError:
            return False

    def validaterh(self, new_text):
        if not new_text:
            self.rh = 0
            return True
        
        try: 
            self.rh = float(new_text)
            self.hr = Psychro.get_humidity_ratio(self.temp, self.rh)
            self.update()
            return True

        except ValueError:
            return False

    def update(self):
        self.total_label_text.set(self.hr)

root = Tk()
my_gui = Calculator(root)
root.mainloop()
        
 