'''
Based on tk_counter_down101.py
count down seconds from a given minute value
using the Tkinter GUI toolkit that comes with Python
tested with Python27 and Python33
'''

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
import shelve
import time
import Queue
import random




class DefiningTheMob:
    def __init__(self, parent, my_config):
        top = self.top = tk.Toplevel(parent)



        self.myLabel = tk.Label(top, text='Enter comma separated list of mom members below')
        self.myLabel.pack()

        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.myEntryBox.insert(0, ', '.join(my_config['mob_list']))

        self.myLabel2 = tk.Label(top, text='Enter timer interval in seconds')
        self.myLabel2.pack()

        self.myEntryBox2 = tk.Entry(top)
        self.myEntryBox2.pack()
        self.myEntryBox2.insert(0, my_config['timer_len'])

        self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        # global theMob
        raw = self.myEntryBox.get()
        theMob = raw.split(',')
        my_config['mob_list'] = theMob
        timer_val = self.myEntryBox2.get()
        my_config['timer_len'] = int(timer_val)
        self.top.destroy()


class MobDriver:
    def __init__(self, parent, list_of_mob_members):
        self.parent = parent
        assert isinstance(list_of_mob_members, object)
        self.update_list(list_of_mob_members)
        random.shuffle(self.navigator_list)
        self.index = 0;

    def update_list(self, list_of_mob_members):
        self.navigator_list = list_of_mob_members

    def new_navigator(self):
        top = self.top = tk.Toplevel(self.parent)
        self.top.attributes('-fullscreen', True)
        self.label_font = ('helvetica', 40)
        self.message = tk.StringVar()
        self.index += 1
        if self.index >= len(self.navigator_list) - 1:
            self.index = 0

        self.message.set(self.navigator_list[self.index] + " step right up to drive")
        self.navigatorLabel = tk.Label(self.top, textvariable=self.message, font=self.label_font, bg='white',
                                       fg='blue', relief='raised', bd=3)
        self.navigatorLabel.pack()
        self.mySubmitButton = tk.Button(self.top, text='Get Mobbing', command=self.done)
        self.mySubmitButton.pack()

    def done(self):
        self.top.destroy()
        return


class App:
    def __init__(self,main_window):
        # create root/main window - refactor since we are getting it from main now as we classify this
        #self.root = tk.Tk()
        self.root = main_window
        self.time_str = tk.StringVar()
        self.firsttime= True
        self.timerControl = Queue.Queue()

        # create the time display label, give it a large font
        # label auto-adjusts to the font
        label_font = ('helvetica', 40)
        tk.Label(root, textvariable=self.time_str, font=label_font, bg='white',
                 fg='blue', relief='raised', bd=3).pack(fill='x', padx=5, pady=5)

        # create start,stop, and mob buttons
        # pack() positions the buttons below the label
        tk.Button(root, text='Count Start', command=self.count_down).pack()
        # stop simply exits root window
        # tk.Button(root, text='Count Stop', command=root.destroy).pack()
        tk.Button(root, text='Count Stop', command=self.stop_timer).pack()
        tk.Button(root, text='Configuration', command=self.on_mob_click).pack()
        tk.Button(root, text='Change Driver', command=self.on_change_driver).pack()

        # Catch the closing of the window via Xing out
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # start the GUI event loop
        self.root.mainloop()

    def on_change_driver(self):
        mobcontrol.new_navigator()
        self.root.wait_window(mobcontrol.top)

    def reset_timer(self):
        sf = "{:02d}:{:02d}".format(*divmod(my_config['timer_len'], 60))
        self.time_str.set(sf)
        self.root.update()

    def count_down(self):
        # clear any lingering control messages
        self.timerControl.queue.clear()

        if self.firsttime:
            self.firsttime = False
            self.on_change_driver()

        for t in range(my_config['timer_len'], -1, -1):
            # format as 2 digit integers, fills with zero to the left
            # divmod() gives minutes, seconds
            sf = "{:02d}:{:02d}".format(*divmod(t, 60))
            self.time_str.set(sf)
            self.root.update()
            # delay one second
            try:
                msg = self.timerControl.get(True, 1)
                if msg is not None:
                    self.reset_timer()
                    return
            except:
                pass

        self.reset_timer()
        mobcontrol.new_navigator()


    def stop_timer(self):
        print("Sending stop")
        self.timerControl.put("stop")


    def on_closing(self):
        # minimize before closing
        self.root.wm_state('iconic')
        self.stop_timer()
        # Hack to allow for exiting
        time.sleep(2)
        self.root.destroy()
        print("Timer exiting")


    def on_mob_click(self):
        inputDialog = DefiningTheMob(self.root, my_config)
        self.root.wait_window(inputDialog.top)
        mobcontrol.update_list(my_config['mob_list'])


#
#
# Main
#
#

#only used to seed the config system
defaultMob = ['brendan','hoff','brian','balog']
default_timer_len = 900

#todo refactor
my_config = shelve.open("mobtimer_config")
if my_config.has_key('timer_len') == False:
    my_config['timer_len'] = int(default_timer_len)

if my_config.has_key('mob_list') == False:
    my_config['mob_list'] = defaultMob

# create root/main window
#todo refactor into app class
root = tk.Tk()

# Prepare the Mob
#todo refactor into app class
mobcontrol = MobDriver(root, my_config['mob_list'])

App(root)
exit(0)

