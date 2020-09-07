#!/usr/bin/env python3
# -*- coding: utf8 -*-

from mcpi.minecraft import Minecraft
from mcpi import block

mc = Minecraft.create ()

# posizione di partenza (origine) per tutti i disegni
Ox = 1
Oy = -6
Oz = 48

# costanti che indicano la direzione di sviluppo di un muro (rettangolo di blocchi)
DIR_X = 1
DIR_Y = 2
DIR_Z = 3


def pulisci ( posx, posy, posz ):
    """Cancella tutto per un'area corrispondente a un grosso parallelogramma"""

    mc.setBlocks ( posx - 1, posy, posz - 1, posx + 120, posy + 40, posz + 120, 0 )


def torre ( posx, posy, posz, larghezza = 10, altezza = 20, materiale = block.STONE ):
    """
    Disegna una torre.

    Parametri:

    - posx, posy, posz: coordinate del blocco di partenza alla base della torre;
    - larghezza: larghezza del lato di base della torre;
    - altezza: altezza del muro della torre, parapetto e merlatura esclusi;
    - materiale: ID del materiale da utilizzare.
    """

    # per tenere conto del fatto che un blocco viene disegnato anche nella posizione
    # iniziale posx, posy, posz sottraiamo 1 dalle dimensioni che vengono passate.
    larghezza = larghezza - 1
    altezza = altezza - 1

    # pareti
    mc.setBlocks ( posx, posy, posz, posx + larghezza, posy + altezza, posz, materiale )
    mc.setBlocks ( posx + larghezza, posy, posz, posx + larghezza, posy + altezza, posz + larghezza, materiale )
    mc.setBlocks ( posx, posy, posz, posx, posy + altezza, posz + larghezza, materiale )
    mc.setBlocks ( posx, posy, posz + larghezza, posx + larghezza, posy + altezza, posz + larghezza, materiale )

    # tetto
    mc.setBlocks ( posx, posy + altezza, posz, posx + larghezza, posy + altezza, posz + larghezza, materiale )

    # parapetto
    mc.setBlocks ( posx - 1, posy + altezza + 1, posz - 1, posx + larghezza + 1, posy + altezza + 1, posz - 1, materiale )
    mc.setBlocks ( posx + larghezza + 1, posy + altezza + 1, posz - 1, posx + larghezza + 1, posy + altezza + 1, posz + larghezza + 1, materiale )
    mc.setBlocks ( posx - 1, posy + altezza + 1, posz - 1, posx - 1, posy + altezza + 1, posz + larghezza + 1, materiale )
    mc.setBlocks ( posx - 1, posy + altezza + 1, posz + larghezza + 1, posx + larghezza + 1, posy + altezza + 1, posz + larghezza + 1, materiale )

    # merlatura
    for t in range ( larghezza + 3 ):
        if t % 2:
            mc.setBlocks ( posx - 1 + t, posy + altezza + 2, posz - 1, posx - 1 + t, posy + altezza + 3, posz - 1, materiale )
            mc.setBlocks ( posx + larghezza + 1, posy + altezza + 2, posz - 1 + t, posx + larghezza + 1, posy + altezza + 3, posz - 1 + t, materiale )
            mc.setBlocks ( posx - 1, posy + altezza + 2, posz - 1 + t, posx - 1, posy + altezza + 3, posz + - 1 + t, materiale )
            mc.setBlocks ( posx - 1 + t, posy + altezza + 1, posz + larghezza + 1, posx - 1 + t, posy + altezza + 3, posz + larghezza + 1, materiale )
            

def muro ( posx, posy, posz, direzione = DIR_X, lunghezza = 10, altezza = 15, materiale = block.STONE ):
    """
    Disegna un muro (rettangolo di blocchi).

    Parametri:

    - posx, posy, posz: coordinate del blocco di partenza alla base del muro;
    - direzione: costante che indica la direzione di sviluppo del muro:

      + DIR_X: il muro si sviluppa lungo l'asse X;
      + DIR_Y: il muro si sviluppa lungo l'asse Y; in questo caso il muro è orizzontale
               e non viene aggiunta la merlatura;
      + DIR_Z: il muro si sviluppa lungo l'asse Z;

    - lunghezza: lunghezza del muro;
    - altezza: altezza del muro, merlatura esclusa;
    - materiale: ID del materiale da utilizzare.
    """

    # per tenere conto del fatto che un blocco viene disegnato anche nella posizione
    # iniziale posx, posy, posz sottraiamo 1 dalle dimensioni che vengono passate.
    lunghezza = lunghezza - 1
    altezza = altezza - 1

    if direzione == DIR_X:
        # muro
        mc.setBlocks ( posx, posy, posz, posx + lunghezza, posy + altezza, posz, materiale )

        # merlatura
        for t in range ( lunghezza + 1 ):
            if t % 2:
                mc.setBlocks ( posx + t, posy + altezza, posz, posx + t, posy + altezza + 2, posz, materiale )

    elif direzione == DIR_Z:
        # muro
        mc.setBlocks ( posx, posy, posz, posx, posy + altezza, posz + lunghezza, materiale )

        # merlatura
        for t in range ( lunghezza + 1 ):
            if t % 2:
                mc.setBlocks ( posx, posy + altezza, posz + t, posx, posy + altezza + 2, posz + t, materiale )

    elif direzione == DIR_Y:
        # muro. Niente merlatura per un "muro" orizzontale (è una specie di pavimento)
        mc.setBlocks ( posx, posy, posz, posx + lunghezza, posy, posz + altezza, materiale )


def porta ( posx, posy, posz, direzione = DIR_X, larghezza = 10, altezza = 15 ):
    """
    Disegna una porta. In pratica cancella un rettangolo di blocchi creando un buco.

    Parametri:

    - posx, posy, posz: coordinate del blocco di partenza alla base della porta;
    - direzione: costante che indica la direzione di sviluppo della porta:

      + DIR_X: la porta si sviluppa lungo l'asse X;
      + DIR_Y: la porta si sviluppa lungo l'asse Y; in questo caso la porta è orizzontale
      + DIR_Z: la porta si sviluppa lungo l'asse Z;

    - larghezza: larghezza della porta;
    - altezza: altezza della porta;
    - materiale: ID del materiale da utilizzare.
    """

    # per tenere conto del fatto che un blocco viene disegnato anche nella posizione
    # iniziale posx, posy, posz sottraiamo 1 dalle dimensioni che vengono passate.
    larghezza = larghezza - 1
    altezza = altezza - 1

    if direzione == DIR_X:
        mc.setBlocks ( posx, posy, posz, posx + larghezza, posy + altezza, posz, 0 )
    elif direzione == DIR_Z:
        mc.setBlocks ( posx, posy, posz, posx, posy + altezza, posz + larghezza, 0 )
    elif direzione == DIR_Y:
        mc.setBlocks ( posx, posy, posz, posx + larghezza, posy, posz + altezza, 0 )



def main ():
    larghezza_torre = 10
    lunghezza_muro = 80
    altezza_muro = 15
    larghezza_porta = 10

    pulisci ( Ox, Oy, Oz )

    # i disegni rappresentano i pezzi del castello dall'alto, man mano che vengono aggiuti

    # +--+
    # |  |
    # +--+
    torre ( Ox, Oy, Oz, larghezza = larghezza_torre )
    # +--+                  
    # |  |------------------
    # +--+                  
    muro ( Ox + larghezza_torre, Oy, Oz + 2, DIR_X, lunghezza = lunghezza_muro, altezza = altezza_muro )
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    torre ( Ox + larghezza_torre + lunghezza_muro, Oy, Oz, larghezza = larghezza_torre )
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    #                         |
    #                         |
    #                         |
    #                         |
    #                         |
    #                         |
    muro ( Ox + larghezza_torre + lunghezza_muro + larghezza_torre - 2, Oy, Oz + larghezza_torre, DIR_Z, lunghezza = lunghezza_muro, altezza = altezza_muro )
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    #                         |
    #                         |
    #                         |
    #                         |
    #                         |
    #                         |
    #                       +--+
    #                       |  |
    #                       +--+
    torre ( Ox + larghezza_torre + lunghezza_muro, Oy, Oz + larghezza_torre + lunghezza_muro )
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #                       +--+
    #                       |  |
    #                       +--+
    muro ( Ox + 2, Oy, Oz + larghezza_torre, DIR_Z, lunghezza = lunghezza_muro, altezza = altezza_muro )
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    # +--+                  +--+
    # |  |                  |  |
    # +--+                  +--+
    torre ( Ox, Oy, Oz + larghezza_torre + lunghezza_muro, larghezza = larghezza_torre )
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    muro ( Ox + larghezza_torre, Oy, Oz + larghezza_torre + lunghezza_muro + larghezza_torre - 2, DIR_X, lunghezza= lunghezza_muro, altezza = altezza_muro )
    # +--+                  +--+
    # |  |------------------|  |
    # +--+                  +--+
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    #  |                      |
    # +--+                  +--+
    # |  |-------    -------|  |
    # +--+                  +--+
    porta ( Ox + larghezza_torre + lunghezza_muro / 2 - larghezza_porta / 2, Oy, Oz + larghezza_torre + lunghezza_muro + larghezza_torre - 2, DIR_X, larghezza = larghezza_porta, altezza = altezza_muro - 5 )


    # edificio centrale

    pos_casa_x = Ox + larghezza_torre + 20
    pos_casa_y = Oy
    pos_casa_z = Oz + larghezza_torre + 20
    lunghezza_casa = lunghezza_muro - 40
    altezza_casa = 10
    muro ( pos_casa_x, pos_casa_y, pos_casa_z, DIR_X, lunghezza = lunghezza_casa, altezza = altezza_casa )
    muro ( pos_casa_x + lunghezza_casa - 1, pos_casa_y, pos_casa_z, DIR_Z, lunghezza = lunghezza_casa, altezza = altezza_casa )
    muro ( pos_casa_x, pos_casa_y, pos_casa_z, DIR_Z, lunghezza = lunghezza_casa, altezza = altezza_casa )
    muro ( pos_casa_x, pos_casa_y, pos_casa_z + lunghezza_casa - 1, DIR_X, lunghezza = lunghezza_casa, altezza = altezza_casa )
    porta ( pos_casa_x + lunghezza_casa / 2 - 5, pos_casa_y, pos_casa_z + lunghezza_casa - 1, DIR_X, larghezza = 10, altezza = altezza_casa - 2 )

    h = 0
    for t in range ( lunghezza_casa // 2 ):
        if t % 3 == 0: h = h + 1
        # superficie del tetto
        mc.setBlocks ( pos_casa_x + t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z, pos_casa_x + t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z + lunghezza_casa - 1, block.STONE )
        mc.setBlocks ( pos_casa_x + lunghezza_casa - 1 - t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z, pos_casa_x + lunghezza_casa - 1 - t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z + lunghezza_casa - 1, block.STONE )
        # collegamento con la parete sottostante ("timpano" sotto al tetto)
        mc.setBlocks ( pos_casa_x + t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z, pos_casa_x + t, pos_casa_y + altezza_casa - 1, pos_casa_z, block.STONE )
        mc.setBlocks ( pos_casa_x + lunghezza_casa - 1 - t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z, pos_casa_x + lunghezza_casa - 1 - t, pos_casa_y + altezza_casa - 1, pos_casa_z, block.STONE )
        mc.setBlocks ( pos_casa_x + t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z + lunghezza_casa - 1, pos_casa_x + t, pos_casa_y + altezza_casa - 1, pos_casa_z + lunghezza_casa - 1, block.STONE )
        mc.setBlocks ( pos_casa_x + lunghezza_casa - 1 - t, pos_casa_y + altezza_casa - 1 + h, pos_casa_z + lunghezza_casa - 1, pos_casa_x + lunghezza_casa - 1 - t, pos_casa_y + altezza_casa - 1, pos_casa_z + lunghezza_casa - 1, block.STONE )

    # torce per l'illuminazione
    for t in range ( 5, 38, 2 ):
        mc.setBlock ( pos_casa_x + 1, pos_casa_y + altezza_casa - 5, pos_casa_z + t, block.TORCH )
        mc.setBlock ( pos_casa_x + lunghezza_casa - 2, pos_casa_y + altezza_casa - 5, pos_casa_z + t, block.TORCH )
        mc.setBlock ( pos_casa_x + t, pos_casa_y + altezza_casa - 5, pos_casa_z + 1, block.TORCH )

        mc.setBlock ( pos_casa_x + 1, pos_casa_y + 3, pos_casa_z + t, block.TORCH )
        mc.setBlock ( pos_casa_x + lunghezza_casa - 2, pos_casa_y + 3, pos_casa_z + t, block.TORCH )
        mc.setBlock ( pos_casa_x + t, pos_casa_y + 3, pos_casa_z + 1, block.TORCH )

    # buco nel tetto per l'illuminazione
    mc.setBlocks ( pos_casa_x + lunghezza_casa / 2 - 4, pos_casa_y + altezza_casa, pos_casa_z + lunghezza_casa / 2 - 8, pos_casa_x + lunghezza_casa / 2 + 3, pos_casa_y + altezza_casa + 7, pos_casa_z + lunghezza_casa / 2 + 8, 0 )

    


if __name__ == '__main__':
    main ()
