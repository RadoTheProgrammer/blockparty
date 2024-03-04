#from find_vars import auto
#auto(input)
DIMENSIONSX=20
DIMENSIONSZ=20
MUR=1
SOL=2
MODE="solo"
#"solo" or "multi"
ECRITURE="[BlockParty] "
COULEURS=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
COULEURSSTR=["blanc","orange","magenta","bleu clair","jaune","vert clair","rose","gris fonce",
             "gris clair","cyan","violet","bleu fonce","marron","vert fonce","rouge","noir"]
AUTOTEST=False
AUTOPLAY=True
#addid=1113878
scan=False
game=True
perdu=None
PlayersID=[]
mode=MODE.lower().strip()
class CommandError(Exception):
    pass
def verifplay():
    if not game:
        raise CommandError("Vous n'êtes pas entrain de jouer")
def Connection():
    return Minecraft.create()
def scannage1D(xfor,yfor):
    verifplay()
    global scannage,load1D
    #mc=Connection()
    load1D+=1
    for zfor in range(DIMENSIONSZ+2):
        scannage[xfor][yfor].append(mc.getBlockWithData(xscan+xfor,yscan+yfor,zscan+zfor))
    print(load1D)
    load1D-=1
def scannage2D(xfor):
    verifplay()
    global scannage,load2D
    load2D+=1
    for yfor in range(8):
        scannage[xfor].append([])
        lastload=load1D
        Thread(scannage1D,(xfor,yfor))
        while lastload==load1D:
            pass
    load2D-=1
def scannage3D():
    verifplay()
    global scannage,load3D,load2D,load1D
    scannage=[]
    load3D=1
    load2D=0
    load1D=0
    for xfor in range(DIMENSIONSX+2):
        scannage.append([])
        lastload=load2D
        Thread(scannage2D,(xfor,))
        while lastload==load2D:
            pass
"""def scannage(xfor):
    verifplay()
    global scannages
    data=[]
    
    for yfor in range(8):
        for zfor in range(DIMENSIONSZ+2):
            data.append(mc.getBlockWithData(xscan+xfor,yscan+yfor,zscan+zfor))
    scannages[x]=data"""
def impression1D(xfor,yfor):
    verifplay()
    global scannage,load1D
    mc=Connection()
    load1D+=1
    for zfor in range(DIMENSIONSZ+2):
        mc.setBlock(xscan+xfor,yscan+yfor,zscan+zfor,scannage[xfor][yfor][zfor])
        scannage[xfor][yfor].append(mc.getBlockWithData(xscan+xfor,yscan+yfor,zscan+zfor))
    load1D-=1
def impression3D():
    verifplay()
    global scannage,load3D,load2D,load1D
    load3D=1
    load2D=0
    load1D=0
    for xfor in range(DIMENSIONSX+2):
        lastload=load2D
        Thread(scannage2D,(xfor,))
        while lastload==load2D:
            pass
def impression2D(xfor):
    verifplay()
    global scannage,load2D
    load2D+=1
    for yfor in range(8):
        lastload=load1D
        Thread(impression1D,(xfor,yfor))
        while lastload==load1D:
            pass
    load2D-=1
"""def impression(xfor):
    verifplay()
    idx=0
    scannage=scannages[xfor]
    for y in range(8):
        for z in range(DIMENSIONSZ+2):
            mc.setBlock(xscan+x,yscan+y,zscan+z,scannage[idx])
            idx+=1"""
def Thread(target,args=()):
    _Thread(target=target,args=args).start()
from mcpi.minecraft import Minecraft
from threading import Thread as _Thread
from random import choice
from time import sleep#,time
#mc=Connection()
def terrain(mc):
    verifplay()
    mc.setBlocks(x,y-5,z,x+DIMENSIONSX-1,y-5,z+DIMENSIONSZ-1,1)
    mc.setBlocks(x,y-3,z,x+DIMENSIONSX-1,y-3,z+DIMENSIONSZ-1,0)
    mc.setBlocks(x,y-4,z,x+DIMENSIONSX-1,y-4,z+DIMENSIONSZ-1,0)
    mc.setBlocks(x,y-1,z,x+DIMENSIONSX-1,y-1,z+DIMENSIONSZ-1,SOL)
    mc.setBlocks(x-1,y,z-1,x+DIMENSIONSX,y+1,z+DIMENSIONSZ,MUR)
    mc.setBlocks(x,y,z,x+DIMENSIONSX-1,y+3,z+DIMENSIONSZ-1,0)
          
def name(id,mc):
    verifplay()
    return mc.entity.getName(id)
def getPlayersEntityIds():
    verifplay()
    mc=Connection()
    global allPlayersID,PlayersID,PlayersPos,perdu
    while True:
        try:
            allPlayersID=mc.getPlayerEntityIds()
        except:
            allPlayersID=[]
        #allPlayersID=[*mc.getPlayerEntityIds(),addid]
        events=mc.events.pollChatPosts()
        for event in events:
            id=event.entityId
            if event.message=="leave" and id in PlayersID:
                index=PlayersID.index(id)
                mc.entity.setPos(id,PlayersPos[index])
                del PlayersID[index]
                del PlayersPos[index]
                if perdu!=None:
                    perdu+=1
        if not game:
            break

def verif(id):
    verifplay()
    mc=Connection()
    pseudo=name(id,mc)
    global PlayersID,PlayersPos,gameover,perdu
    dead=False
    while True:
        if not game:
            break
        if not isplay and dead:
            dead=False
        if id not in allPlayersID:
            #print("a")
            index=PlayersID.index(id)
            del PlayersID[index]
            del PlayersPos[index]
            quit(pseudo,mc)
            #print("d")
            break
        elif id not in PlayersID:
            quit(pseudo,mc)
            break
        elif isplay and not dead:
            pos=mc.entity.getTilePos(id)
            if pos.y<y-1:
                perdu+=1
                mc.postToChat(ECRITURE+name(id,mc)+" a perdu, son score: "+str(score))
                mc.entity.setTilePos(id,x-1,y+2,z-1)
                dead=True
            elif len(PlayersID)-perdu==1:
                gameover=True
                #print("aaaaaaaaa")
                mc.postToChat(ECRITURE+name(id,mc)+" a gagne, son score: "+str(score))
                #print("bbbbbbbb")
                dead=True
        
def quit(pseudo,mc):
    verifplay()
    #print("b")
    #n=name(id,mc)
    #print("f")
    mc.postToChat(ECRITURE+pseudo+" a quitte")
    #print("c")
def timer(secs):
    verifplay()
    global timer_run,succeess
    mc=Connection()
    for time in range(secs):
        mc.postToChat(ECRITURE+"lancement: "+str(secs-time))
        sleep(1)
        if mode=="multi" and len(PlayersID)<2:
            mc.postToChat(ECRITURE+"lancement: annule")
            timer_run=False
            break
        if stop:
            break
    if mode=="multi" and timer_run:
        succeess=True
def test():
    from mcpi.minecraft import Minecraft
    mc=Connection()
    ids=mc.getPlayerEntityIds()
    id=ids[0]
    name=mc.entity.getName(id)
    pos=mc.entity.getPos(id) 
    pos2=mc.entity.getTilePos(id)
    mc.entity.setTilePos(id,pos2)
    mc.entity.setPos(id,pos)
    posts=mc.events.pollChatPosts()
    pos3=mc.player.getTilePos()
    posts2=mc.player.pollChatPosts()
    block=mc.getBlockWithData(20,20,20)
    block2=mc.getBlockWithData(20,21,20)
    mc.setBlocks(20,20,20,20,21,20)
    mc.setBlock(20,20,20,block)
    mc.setBlock(20,21,20,block2)
    mc.postToChat("Les fonctions marchent avec succes")
    print("Les fonctions marchent avec succès")
if AUTOTEST:
    test()
def LesCouleurs(mc):
    global score
    _sleep=5
    score=0
    while True:
        mc.postToChat(ECRITURE+"Delai : "+str(round(_sleep,1))+" seconde(s)")
        mc.setBlocks(x,y-3,z,x+DIMENSIONSX-1,y-3,z+DIMENSIONSZ-1,1)
        plateforme=choice(COULEURS)
        for xcons in range(DIMENSIONSX):
            for zcons in range(DIMENSIONSZ):
                couleur=choice(COULEURS)
                mc.setBlock(x+xcons,y-1,z+zcons,252,couleur)
                if plateforme==couleur:
                    mc.setBlock(x+xcons,y-2,z+zcons,1)
                else:
                    mc.setBlock(x+xcons,y-2,z+zcons,13)
        mc.postToChat(ECRITURE+COULEURSSTR[COULEURS.index(plateforme)])
        sleep(_sleep)
        if stop:
            break
        mc.setBlocks(x,y-3,z,x+DIMENSIONSX-1,y-3,z+DIMENSIONSZ-1,0)
        sleep(3)
        if not isplay or (mode=="multi" and gameover) or stop:
            break
        mc.setBlocks(x,y-4,z,x+DIMENSIONSX-1,y-3,z+DIMENSIONSZ-1,0)
        if _sleep>1:
            _sleep-=0.1
        score+=1
    sleep(6)
def verifsolo():
    verifplay()
    global isplay,stop
    mc=Connection()
    dead=False
    while True:
        if not isplay and dead:
            dead=False
        if isplay and not dead:
            pos=mc.player.getTilePos()
            if pos.y<y-1:
                dead=True
                isplay=False
                mc.postToChat(ECRITURE+"Tu as perdu, score:"+str(score))
        events=mc.player.pollChatPosts()
        for event in events:
            if event.message=="stop":
                stop=True
                mc.postToChat(ECRITURE+"Jeu fini")
                print("Jeu fini")
                break
        if stop:
            break
if mode=="solo":
    def play():
        verifplay()
        global x,y,z,xscan,yscan,zscan,isplay,gameover,stop
        stop=False
        isplay=False
        mc=Connection()
        xspawn,yspawn,zspawn=mc.player.getTilePos()
        x=xspawn-int(DIMENSIONSX/2)
        y=yspawn-0
        z=zspawn-int(DIMENSIONSZ/2)
        xscan,yscan,zscan=x-1,y-5,z-1
        mc.player.clearEvents()
        Thread(verifsolo)
        if scan:
            scannage3D()
            while load3D+load2D+load1D>0:
                input()
        while True:
            mc.postToChat(ECRITURE+"Nouvelle partie")
            terrain(mc)
            mc.player.setTilePos(xspawn,yspawn,zspawn)
            timer(3)
            isplay=True
            LesCouleurs(mc)
            if stop:
                break
        if scan:
            impression3D()
        else:
            mc.setBlocks(xscan,yscan,zscan,xscan+DIMENSIONSX+1,yscan+7,zscan+DIMENSIONSZ+1,0)
        print("Jeu fini")
elif mode=="multi":
    def play():
        global xscan,yscan,zscan,game,allPlayersID,PlayersID,PlayersPos,timer_run,succeess,gameover,scannages,x,y,z,perdu,isplay,score,stop
        game=True
        mc=Connection()
        allPlayersID,PlayersID,PlayersPos=[],[],[]
        xspawn,yspawn,zspawn=mc.player.getTilePos()
        x=xspawn-int(DIMENSIONSX/2)
        y=yspawn-0
        z=zspawn-int(DIMENSIONSZ/2)
        scannages=[]
        stop=False
        xscan,yscan,zscan=x-1,y-5,z-1
        if scan:
            scannage3D()
            while load3D+load2D+load1D>0:
                input()
        #terrain(mc)
        Thread(getPlayersEntityIds)
        print("Nouvelle partie")
        while True:
            terrain(mc)
            isplay=False
            timer_run=False
            succeess=False
            gameover=False
            perdu=None
            #mc=Connection()
            terrain(mc)
            mc.postToChat(ECRITURE+"Nouvelle partie")
            for id in PlayersID:
                mc.entity.setTilePos(id,xspawn,yspawn,zspawn)
                mc.postToChat(ECRITURE+name(id,mc)+" a rejoint")
                if (len(PlayersID)>1 and not timer_run):
                    timer_run=True
                    Thread(timer,(10,))
            mc.events.clearAll()
            while True:
                events=mc.events.pollChatPosts()
                #print(events)
                for event in events:
                    id=event.entityId
                    if event.message=="play" and id not in PlayersID:
                        #print("ww")
                        PlayersID.append(id)
                        PlayersPos.append(mc.entity.getPos(id))
                        mc.entity.setTilePos(id,xspawn,yspawn,zspawn)
                    
                        Thread(verif,(id,))
                        mc.postToChat(ECRITURE+name(id,mc)+" a rejoint depuis x:"+str(PlayersPos[-1].x)+" y:"+str(PlayersPos[-1].y)+" z:"+str(PlayersPos[-1].z))
                        #Vous devez enlever:
                        """id=addid
                        PlayersID.append(id)
                        PlayersPos.append(mc.entity.getPos(id))
                        mc.entity.setTilePos(id,x,y,z)
                        verif_Thread=Thread(target=verif,args=(id,))
                        verif_Thread.start()
                        mc.postToChat(name(id)+" a rejoint")"""
                        #OK ?
                        if (len(PlayersID)>1 and not timer_run):
                            timer_run=True
                            Thread(timer,(10,))
                    elif event.message=="stop":
                        #print("e")
                        #n=name(id,mc)
                        #mc.postToChat(ECRITURE+n+" demande d'arrêter le jeu, le chef doit confirmer sur Python")
                        stop=True
                        break
                if succeess:
                    break
                if stop:
                    break
            if stop:
                break
            perdu=0
            isplay=True
            mc.postToChat(ECRITURE+"Partie lance")
            #mc.player.setTilePos(x,y,z)
            LesCouleurs(mc)

        #for xfor in range(DIMENSIONSX+2):
        #    impression_Thread=Thread(target=impression,args=(xfor,))
        #    impression_Thread.start()
        if scan:
            impression3D()
        else:
            mc.setBlocks(xscan,yscan,zscan,xscan+DIMENSIONSX+1,yscan+7,zscan+DIMENSIONSZ+1,0)
        print("Jeu fini")
        mc.postToChat(ECRITURE+"Jeu fini")
        for id in PlayersID:
            mc.entity.setPos(id,PlayersPos[index])
            PlayersID.remove(id)
            PlayersPos.remove(pos)
        game=False
else:
    raise CommandError("Le mode "+mode+" n'est pas valide")
if AUTOPLAY:
    play()
game=False
                
