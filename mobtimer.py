"""
Based on tk_counter_down101.py
count down seconds from a given minute value
using the Tkinter GUI toolkit that comes with Python
tested with Python27 and Python33
"""

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
import shelve
import time
import random


class DefiningTheMob:
    """ GUI to enter parameters that define the Mob and how they work


    :param parent: Parent window
    :param my_config: Shelve object
    :return: None
    """
    def __init__(self, parent, my_config):

        top = self.top = tk.Toplevel(parent)
        self.config = my_config

        tk.Label(top, text='Enter comma separated list of Mob members below').pack()
        self.myMoblistEntry = tk.Entry(top, width=100)
        self.myMoblistEntry.pack()
        self.myMoblistEntry.insert(0, ', '.join(self.config['mob_list']))

        tk.Label(top, text='Enter timer interval in seconds').pack()
        self.myTimerEntry = tk.Entry(top)
        self.myTimerEntry.pack()
        self.myTimerEntry.insert(0, self.config['timer_len'])

        self.mySubmitButton = tk.Button(top, text='Submit', command=self.submit)
        self.mySubmitButton.pack()

    def submit(self):
        raw = self.myMoblistEntry.get()
        themob = raw.split(',')
        self.config['mob_list'] = themob
        timer_val = self.myTimerEntry.get()
        self.config['timer_len'] = int(timer_val)
        self.top.destroy()


class MobDriver:
    def __init__(self, parent, list_of_mob_members):
        self.parent = parent
        self.navigator_list = list_of_mob_members
        self.index = 0
        self.label_font = ('helvetica', 40)
        self.message = tk.StringVar()

        # suppress instance attribute defined outside of __init__ warnings
        self.top = None
        self.navigatorLabel = None
        self.mySubmitButton = None

        random.shuffle(self.navigator_list)

    def update_list(self, list_of_mob_members):
        self.navigator_list = list_of_mob_members

    def new_navigator(self):
        self.top = tk.Toplevel(self.parent)
        self.top.attributes('-fullscreen', True)

        self.index += 1
        if self.index >= len(self.navigator_list) - 1:
            self.index = 0

        self.message.set(self.navigator_list[self.index] + " step right up to drive")
        self.navigatorLabel = tk.Label(self.top, textvariable=self.message, font=self.label_font, bg='white',
                                       fg='blue', relief='raised', bd=3)
        padding = self.top.winfo_screenmmheight() / 2
        self.navigatorLabel.pack(pady=padding)
        self.mySubmitButton = tk.Button(self.top, text='Get Mobbing', command=self.done)
        self.mySubmitButton.pack()

    def done(self):
        self.top.destroy()
        return


class MobTimer:
    """ Main class of the application

    """
    def __init__(self, main_window, configuration_shelve):
        self.root = main_window
        self.config = configuration_shelve
        self.root.title('Mob Programming Timer')
        self.time_str = tk.StringVar()
        self.firsttime = True
        self.paused = False
        self.stopped = False
        self.mobdriver   = MobDriver(root, self.config['mob_list'])
        # create the time display label, give it a large font
        # label auto-adjusts to the font
        label_font = ('helvetica', 40)
        tk.Label(root, textvariable=self.time_str, font=label_font, bg='white',
                 fg='blue', relief='raised', bd=3).pack(fill='x', padx=5, pady=5)

        # create start,stop, and mob buttons
        # pack() positions the buttons below the label
        tk.Button(root, text='Counter Start', command=self.start_timer).pack()
        tk.Button(root, text='Counter Stop', command=self.stop_timer).pack()
        tk.Button(root, text='Counter Pause', command=self.pause_timer).pack()
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
        sf = "{:02d}:{:02d}".format(*divmod(self.config['timer_len'], 60))
        self.time_str.set(sf)
        self.root.update()

    def count_down(self):
        my_time_countdown = self.config['timer_len']

        if self.firsttime:
            self.firsttime = False
            self.on_change_driver()

        while my_time_countdown > -1:
            # format as 2 digit integers, fills with zero to the left
            # divmod() gives minutes, seconds
            sf = "{:02d}:{:02d}".format(*divmod(my_time_countdown, 60))
            self.time_str.set(sf)
            self.root.update()
            # delay one second
            for ll in range(0, 4):
                if self.stopped:
                    self.paused = self.stopped = False
                    self.reset_timer()
                    return
                time.sleep(0.250)

            if not self.paused:
                my_time_countdown -= 1

        self.reset_timer()
        mobcontrol.new_navigator()

    def stop_timer(self):
        self.stopped = True

    def pause_timer(self):
        self.paused = True

    def start_timer(self):
        if self.paused:
            # restart paused timer
            self.paused = False
        else:
            # start new timer
            self.count_down()

    def on_closing(self):
        # minimize before closing
        # self.root.wm_state('iconic')
        self.root.withdraw()
        self.stop_timer()
        time.sleep(1)
        self.root.quit()

    def on_mob_click(self):
        inputdialog = DefiningTheMob(self.root, self.config)
        self.root.wait_window(inputdialog.top)
        mobcontrol.update_list(self.config['mob_list'])


#
#
# Main
#
#

# Establish default configuration if needed
# only used to seed the config system
defaultMob = ['Jane', 'Joe', 'Julie', 'Jack']
default_timer_len = 900

app_config = shelve.open("mobtimer_config")
if not app_config.has_key('timer_len'):
    app_config['timer_len'] = int(default_timer_len)

if not app_config.has_key('mob_list'):
    app_config['mob_list'] = defaultMob

# create root/main window
# todo refactor into app class
root = tk.Tk()

# Prepare the Mob
# todo refactor into app class
mobcontrol = MobDriver(root, app_config['mob_list'])

MobTimer(root, app_config)
root.destroy()

print("Timer exiting")
exit(0)
