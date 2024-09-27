import os
import subprocess
import shutil


username = "toor" #@param {type:"string"}
password = "root" #@param {type:"string"}
os.system(f"useradd -m {username}")
os.system(f"adduser {username} sudo")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")


CRP = ''

Pin = 123456 #@param {type: "integer"}
Autostart = True #@param {type: "boolean"}


class CRD:
    def __init__(self, user):
        os.system("apt update")
        self.installCRD()
        self.installDesktopEnvironment()
        self.installGoogleChrome()
        self.installCoApp()
        self.installXDManager()
        self.finish(user)

    @staticmethod
    def installCRD():
        print("Installing Chrome Remote Desktop")
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
        os.remove('chrome-remote-desktop_current_amd64.deb')

    @staticmethod
    def installDesktopEnvironment():
        print("Installing Desktop Environment")
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal xfce4-goodies xorg dbus-x11 x11-xserver-utils gedit")
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("systemctl disable lightdm.service")

    @staticmethod
    def installGoogleChrome():
        print("Installing Google Chrome")
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
        os.remove('google-chrome-stable_current_amd64.deb')

    @staticmethod
    def installCoApp():
        print("Installing CoApp")
        subprocess.run(["wget", "https://github.com/aclap-dev/vdhcoapp/releases/latest/download/vdhcoapp-linux-x86_64.deb"], stdout=subprocess.PIPE)
        subprocess.run(["dpkg", "--install", "vdhcoapp-linux-x86_64.deb"], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
        os.remove('vdhcoapp-linux-x86_64.deb')

    @staticmethod
    def installXDManager():
        print("Installing XDM")
        subprocess.run(["wget", "https://raw.githubusercontent.com/barcuranja/neofetch/main/xdman.deb"], stdout=subprocess.PIPE)
        subprocess.run(["dpkg", "--install", "xdman.deb"], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
        os.remove('xdman.deb')

    @staticmethod
    def finish(user):
        print("Finalizing")
        if Autostart:
            os.makedirs(f"/home/{user}/.config/autostart", exist_ok=True)
            link = "https://www.google.com/"
            colab_autostart = """[Desktop Entry]
Type=Application
Name=Colab
Exec=sh -c "sensible-browser {}"
Icon=
Comment=Open a predefined notebook at session signin.
X-GNOME-Autostart-enabled=true""".format(link)
            with open(f"/home/{user}/.config/autostart/colab.desktop", "w") as f:
                f.write(colab_autostart)
            os.system(f"chmod +x /home/{user}/.config/autostart/colab.desktop")
            os.system(f"chown {user}:{user} /home/{user}/.config")

        os.system(f"adduser {user} chrome-remote-desktop")
        command = f"{CRP} --pin={Pin}"
        os.system(f"su - {user} -c '{command}'")
        os.system("service chrome-remote-desktop start")
        

        print("Finished Succesfully")

        while True:pass

try:
    if CRP == "":
        print("Please enter authcode from the given link")
    elif len(str(Pin)) < 6:
        print("Enter a pin more or equal to 6 digits")
    else:
        CRD(username)
except NameError as e:
    print("'username' variable not found, Create a user first")
