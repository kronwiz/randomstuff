import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class MyWorld here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class MyWorld extends World
{

    /**
     * Constructor for objects of class MyWorld.
     * 
     */
    public MyWorld()
    {
        // Create a new world with a cell size of 35 pixels.
        super(50, 50, 35);
        
        drawMaze();
    }

    private void drawMaze () {
        MazeGenerator maze = new MazeGenerator ( 8, 8 );
        maze.render ( this );
    }

    /* Da sistemare, dovrebbe restituire la dimensione di World ma dovrebbe essere chiamata prima di "super", cosa che non si può fare */
    private Integer[] calcSize () {
        int maze_width = 8; // unit: maze cells
        int maze_height = 8; // unit: maze cells
        int maze_cell_width = 2; // unit: world cells

        Integer[] ar = new Integer[2];  // TODO
        ar [ 0 ] = 0;
        ar [ 1 ] = 1;
        return ar;
    }

}
