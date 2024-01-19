import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

import processing.core.*;

public final class VirtualWorld extends PApplet {
    private static String[] ARGS;

    public static final int VIEW_WIDTH = 640;
    public static final int VIEW_HEIGHT = 480;
    public static final int TILE_WIDTH = 32;
    public static final int TILE_HEIGHT = 32;

    public static final int VIEW_COLS = VIEW_WIDTH / TILE_WIDTH;
    public static final int VIEW_ROWS = VIEW_HEIGHT / TILE_HEIGHT;

    public static final String IMAGE_LIST_FILE_NAME = "imagelist";
    public static final String DEFAULT_IMAGE_NAME = "background_default";
    public static final int DEFAULT_IMAGE_COLOR = 0x808080;

    public static final String FAST_FLAG = "-fast";
    public static final String FASTER_FLAG = "-faster";
    public static final String FASTEST_FLAG = "-fastest";
    public static final double FAST_SCALE = 0.5;
    public static final double FASTER_SCALE = 0.25;
    public static final double FASTEST_SCALE = 0.10;

    private static final int KEYED_RED_IDX = 2;
    private static final int KEYED_GREEN_IDX = 3;
    private static final int KEYED_BLUE_IDX = 4;
    public static final int KEYED_IMAGE_MIN = 5;

    public String loadFile = "world.sav";
    public long startTimeMillis = 0;
    public double timeScale = 1.0;

    public ImageStore imageStore;
    public WorldModel world;
    public WorldView view;
    public EventScheduler scheduler;

    /*
          Called with color for which alpha should be set and alpha value.
          setAlpha(img, color(255, 255, 255), 0));
        */
    public void setAlpha(PImage img, int maskColor, int alpha) {
        int alphaValue = alpha << 24;
        int nonAlpha = maskColor & Functions.COLOR_MASK;
        img.format = ARGB;
        img.loadPixels();
        for (int i = 0; i < img.pixels.length; i++) {
            if ((img.pixels[i] & Functions.COLOR_MASK) == nonAlpha) {
                img.pixels[i] = alphaValue | nonAlpha;
            }
        }
        img.updatePixels();
    }

    public void processImageLine(Map<String, List<PImage>> images, String line, PApplet screen) {
        String[] attrs = line.split("\\s");
        if (attrs.length >= 2) {
            String key = attrs[0];
            PImage img = screen.loadImage(attrs[1]);
            if (img != null && img.width != -1) {
                List<PImage> imgs = getImages(images, key);
                imgs.add(img);

                if (attrs.length >= KEYED_IMAGE_MIN) {
                    int r = Integer.parseInt(attrs[KEYED_RED_IDX]);
                    int g = Integer.parseInt(attrs[KEYED_GREEN_IDX]);
                    int b = Integer.parseInt(attrs[KEYED_BLUE_IDX]);
                    setAlpha(img, screen.color(r, g, b), 0);
                }
            }
        }
    }
    public List<PImage> getImages(Map<String, List<PImage>> images, String key) {
        return images.computeIfAbsent(key, k -> new LinkedList<>());
    }
    public void settings() {
        size(VIEW_WIDTH, VIEW_HEIGHT);
    }

    /*
       Processing entry point for "sketch" setup.
    */
    public void setup() {
        parseCommandLine(ARGS);
        loadImages(IMAGE_LIST_FILE_NAME);
        loadWorld(loadFile, this.imageStore);

        this.view = new WorldView(VIEW_ROWS, VIEW_COLS, this, world, TILE_WIDTH, TILE_HEIGHT);
        this.scheduler = new EventScheduler();
        this.startTimeMillis = System.currentTimeMillis();
        this.scheduleAllActions(world, scheduler, imageStore);
    }

    public void draw() {
        double appTime = (System.currentTimeMillis() - startTimeMillis) * 0.001;
        double frameTime = (appTime - scheduler.currentTime())/timeScale;
        this.update(frameTime);
        view.drawViewport();
    }

    public void update(double frameTime){
        scheduler.updateOnTime(frameTime);
    }

    // Just for debugging and for P5
    // Be sure to refactor this method as appropriate
    public void mousePressed() {
        Point pressed = mouseToPoint();
        System.out.println("CLICK! " + pressed.x + ", " + pressed.y);

        Optional<Entity> entityOptional = world.getOccupant(pressed);
        if (entityOptional.isPresent()) {
            Entity entity = entityOptional.get();
            System.out.println(entity.getId() + ": " + entity.getKey().toUpperCase() + " : " + entity.getHealth());
        }else{
            clickEvent(pressed);
        }


    }

    public void clickEvent(Point pt){
        clickSpawnNewEntity(pt);
        clickEventBackgroundChange(pt);
        clickTransformNearbyEntities(pt);
    }

    public void clickSpawnNewEntity(Point pt) {
        if(this.world.getBackgroundCell(pt).getImageID().equals("mushrooms")){
            Fairy fairy = new Fairy(Fairy.KIND.toLowerCase(), pt, imageStore.getImageList(Fairy.KIND.toLowerCase()), 0.123, 0.123);
            world.addEntity(fairy);
            ((ActionDoer)fairy).scheduleActions(scheduler, world, imageStore);

        }else{
            Wizard wizard = new Wizard(Wizard.KIND.toLowerCase(), pt, imageStore.getImageList(Wizard.KIND.toLowerCase()), .2, .5);
            world.addEntity(wizard);
            ((ActionDoer)wizard).scheduleActions(scheduler, world, imageStore);
        }
    }
    public void clickTransformNearbyEntities(Point pt) {
        /*List<Point> nearbyEntities = new ArrayList<>(PathingStrategy.DIAGONAL_CARDINAL_NEIGHBORS.apply(pt)
                .filter(p -> world.withinBounds(p) && world.isOccupied(p))
                .filter(p -> world.getOccupancyCell(p).getId().equals(Dude.KIND.toLowerCase()))
                .forEach(p -> System.out.println("Dude Location: " + p))*/;
                //.toList());
        PathingStrategy.DIAGONAL_CARDINAL_NEIGHBORS.apply(pt)
                .filter(p -> world.withinBounds(p) && world.isOccupied(p))
                .filter(p ->
                        world.getOccupancyCell(p).getKey().equals(Dude.KIND.toLowerCase()) ||
                        world.getOccupancyCell(p).getKey().equals(Fairy.KIND.toLowerCase()) ||
                        world.getOccupancyCell(p).getKey().equals(Sapling.KIND.toLowerCase()) ||
                        world.getOccupancyCell(p).getKey().equals(Tree.KIND.toLowerCase()) ||
                        world.getOccupancyCell(p).getKey().equals(Stump.KIND.toLowerCase()) ||
                        world.getOccupancyCell(p).getKey().equals(BigMushroom.KIND.toLowerCase()) ||
                        world.getOccupancyCell(p).getKey().equals(Skeleton.KIND.toLowerCase()) ||
                        world.getOccupancyCell(p).getKey().equals(Wizard.KIND.toLowerCase()))
                .forEach(p -> ((ClickEventTransform)world.getOccupancyCell(p)).clickTransform(world, scheduler, imageStore));

    }
    public void clickEventBackgroundChange(Point pt){
        List<Point> neighbors = new ArrayList<>(PathingStrategy.DIAGONAL_CARDINAL_NEIGHBORS.apply(pt)
                //&& !world.isOccupied(p)
                .filter(p -> world.withinBounds(p) && !world.getBackgroundCell(p).getImageID().equals("bridge"))
                .toList());
        if(neighbors.size()>6){
            int numToRemove = neighbors.size()-6;
            Random rand = new Random();
            for(int i = 0; i<numToRemove; i++){
                int ind = rand.nextInt(0, neighbors.size());
                neighbors.remove(ind);
            }
        }
        neighbors.add(pt);
        if(this.world.getBackgroundCell(pt).getImageID().equals("mushrooms")){
            neighbors.forEach(p -> {
                if(Math.random()>0.5){
                    world.setBackgroundCell(p, new Background("grass", imageStore.getImageList("grass")));
                }else{
                    world.setBackgroundCell(p, new Background("flowers", imageStore.getImageList("flowers")));
                }
            });
        }else{
            neighbors.forEach(p -> world.setBackgroundCell(p, new Background("mushrooms", imageStore.getImageList("mushrooms"))));
        }

    }

    public void scheduleAllActions(WorldModel world, EventScheduler scheduler, ImageStore imageStore) {
        for (Entity entity : world.entities()) {
            try{
                ((ActionDoer)entity).scheduleActions(scheduler, world, imageStore);
            }catch(ClassCastException exc) {

            }
        }
    }

    private Point mouseToPoint() {
        return view.viewport().viewportToWorld(mouseX / TILE_WIDTH, mouseY / TILE_HEIGHT);
    }

    public void keyPressed() {
        if (key == CODED) {
            int dx = 0;
            int dy = 0;

            switch (keyCode) {
                case UP -> dy -= 1;
                case DOWN -> dy += 1;
                case LEFT -> dx -= 1;
                case RIGHT -> dx += 1;
            }
            view.shiftView(dx, dy);
        }
    }

    public static Background createDefaultBackground(ImageStore imageStore) {
        return new Background(DEFAULT_IMAGE_NAME, imageStore.getImageList(DEFAULT_IMAGE_NAME));
    }

    public static PImage createImageColored(int width, int height, int color) {
        PImage img = new PImage(width, height, RGB);
        img.loadPixels();
        Arrays.fill(img.pixels, color);
        img.updatePixels();
        return img;
    }

    public void loadImages(String filename) {
        this.imageStore = new ImageStore(createImageColored(TILE_WIDTH, TILE_HEIGHT, DEFAULT_IMAGE_COLOR));
        try {
            Scanner in = new Scanner(new File(filename));
            imageStore.loadImages(in, this, this);
        } catch (FileNotFoundException e) {
            System.err.println(e.getMessage());
        }
    }

    public void loadWorld(String file, ImageStore imageStore) {
        this.world = new WorldModel();
        try {
            Scanner in = new Scanner(new File(file));
            world.load(in, imageStore, createDefaultBackground(imageStore));
        } catch (FileNotFoundException e) {
            Scanner in = new Scanner(file);
            world.load(in, imageStore, createDefaultBackground(imageStore));
        }
    }

    public void parseCommandLine(String[] args) {
        for (String arg : args) {
            switch (arg) {
                case FAST_FLAG -> timeScale = Math.min(FAST_SCALE, timeScale);
                case FASTER_FLAG -> timeScale = Math.min(FASTER_SCALE, timeScale);
                case FASTEST_FLAG -> timeScale = Math.min(FASTEST_SCALE, timeScale);
                default -> loadFile = arg;
            }
        }
    }

    public static void main(String[] args) {
        VirtualWorld.ARGS = args;
        PApplet.main(VirtualWorld.class);
    }

    public static List<String> headlessMain(String[] args, double lifetime){
        VirtualWorld.ARGS = args;

        VirtualWorld virtualWorld = new VirtualWorld();
        virtualWorld.setup();
        virtualWorld.update(lifetime);

        return virtualWorld.world.log();
    }
}
