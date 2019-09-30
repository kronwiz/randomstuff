from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi.vec3 import Vec3
from minecraftstuff import MinecraftDrawing, MinecraftShape

import os, time

FILE_POS_PLAYER = "pos_player.txt"

# globale cosi' posso usarli ovunque
mc = Minecraft.create ()
mcd = MinecraftDrawing ( mc )


def trova_pos_player ():
    """
    Memorizza in un file di testo le coordinate correnti del player cosi'
    da poterle ricaricare le volte successive.
    Se il file di testo esiste gia' ricarica le coordinate dal file di
    testo.

    Restituisce le coordinate in formato Vec3 (standard Minecraft API).
    """
    
    if os.path.exists ( FILE_POS_PLAYER ):
        print ( """Trovate le coordinate del player memorizzate: le ripristino.
Ricordati di cancellare il file %s se vuoi memorizzare nuove coordinate.""" % FILE_POS_PLAYER )
        fin = open ( FILE_POS_PLAYER, "r" )

        try:
            coords = [ int ( x ) for x in fin.readline ().strip ().split ( "," ) ]
            pos = Vec3 ( *coords )

        except:
            print ( "Errore nella lettura del file %s" % FILE_POS_PLAYER )


    else:
        print ( "Nessuna coordinata memorizzata trovata: memorizzo quelle attuali." )
        pos = mc.player.getTilePos ()
        try:
            fout = open ( "pos_player.txt", "w" )
            coords = "%s,%s,%s" % ( pos.x, pos.y, pos.z )
            fout.write ( "%s\n" % coords )

        except:
            print ( "Errore nella scrittura del file %s" % FILE_POS_PLAYER )

    return pos


def disegna_assi ( pos, cancella = False ):
    mat_x = block.WOOD.id
    mat_y = block.STONE.id
    mat_z = block.SAND.id

    if cancella:
        mat_x = mat_y = mat_z = 0

    # asse x
    mcd.drawLine ( pos.x, pos.y, pos.z, pos.x + 10, pos.y, pos.z, mat_x )
    # asse y
    mcd.drawLine ( pos.x, pos.y, pos.z, pos.x, pos.y + 10, pos.z, mat_y )
    # asse z
    mcd.drawLine ( pos.x, pos.y, pos.z, pos.x, pos.y, pos.z + 10, mat_z )


def main ():
    # disegna_assi ( pos )
    pos = trova_pos_player ()

    # un po' di pulizia
    mc.setBlocks ( pos.x, pos.y, pos.z, pos.x + 25, pos.y + 25, pos.z + 25, 0 )

    # muri
    muro = MinecraftShape ( mc, pos )
    muro.setBlocks ( 0, 0, 0, 10, 20, 0, block.STONE.id )
    muro.setBlocks ( 10, 0, 0, 10, 20, 10, block.STONE.id )
    muro.setBlocks ( 0, 0, 0, 0, 20, 10, block.STONE.id )
    muro.setBlocks ( 0, 0, 10, 10, 20, 10, block.STONE.id )
    # porta
    muro.setBlocks ( 3, 0, 10, 7, 10, 10, 0 )

    # pale del mulino
    davanti_pos = Vec3 ( pos.x + 5, pos.y + 15, pos.z + 11 )
    pale = MinecraftShape ( mc, davanti_pos )
    pale.setBlocks( -10, 0, 0, 10, 0, 0, block.BEDROCK.id )
    pale.setBlocks( 0, -10, 0, 0, 10, 0, block.BEDROCK.id )


    # animiamo le pale
    while 1:
        pale.rotateBy ( 0, 0, 10 )
        time.sleep ( 1 )


if __name__ == '__main__':
    main ()
