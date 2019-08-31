'''
use unsplash api to fetch next wallpaper
create dir /var/opt/repaint
move new wallpaper to /var/opt/repaint/
'''
import subprocess as sub

user_home_dir = get_dir = sub.Popen('echo $HOME', shell=True, stdout=sub.PIPE)
repaint_default_dir = user_home_dir.communicate()[0].decode('ascii').rstrip()
repaint_default_dir = repaint_default_dir + '/repaint'


def call_unsplash():
    print("Calling UnSplash APIs to get the next amazing wallpaper...")
    res = sub.Popen('curl https://api.unsplash.com/photos/random?client_id=cbe31d9f91f95d0d35be45aca596919deff0cf47ee01a684ff8323aec482278f\&query=waves\&orientation=landscape', shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    res2 = sub.Popen('jq -r \'.urls.full\'', stdin=res.stdout, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
    link = res2.communicate()[0].decode('ascii')
    #print('Received link: ', link)
    if(link):
        print('Downloading new wallpaper...')
        command = 'wget -O  {0}/nextWallpaper.jpg {1} > /dev/null'.format(repaint_default_dir, link)
        res3 = sub.Popen(command, shell=True, stdout=sub.PIPE)
        #print(res3.communicate())
    else:
        print('API call failed... Exiting!')


def set_wallpaper():
        print('Setting your next wallpaper...')
        command = "gsettings set org.gnome.desktop.background picture-uri  'file:{}/nextWallpaper.jpg'".format(repaint_default_dir)
        print(command)
        sub.Popen(command, shell=True)
        sub.Popen('cp {0}/nextWallpaper.jpg /var/lib/lightdm-data/$( whoami )/wallpaper/'.format(repaint_default_dir), shell=True)

t = sub.Popen('ls {0}'.format(repaint_default_dir), shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
err = t.communicate()[1].decode('ascii')
dir_exist = (err == '')
if(not dir_exist):
        print('Creating the directory {0}...'.format(repaint_default_dir))
        sub.Popen('mkdir {0}'.format(repaint_default_dir), shell=True)

call_unsplash()
set_wallpaper()
print('Successfully updated wallpaper!')
