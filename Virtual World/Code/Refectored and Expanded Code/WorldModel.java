import processing.core.PImage;

import java.util.*;

/**
 * Represents the 2D World in which this simulation is running.
 * Keeps track of the size of the world, the background image for each
 * location in the world, and the entities that populate the world.
 */
public final class WorldModel {
    private int numRows;
    private int numCols;
    private Background[][] background;
    private Entity[][] occupancy;
    private Set<Entity> entities;

    public WorldModel() {

    }
    public Set<Entity> entities(){return this.entities;}
    public int numRows(){return this.numRows;}
    public int numCols(){return this.numCols;}
    public Entity getOccupancyCell( Point pos) {
        return this.occupancy[pos.y][pos.x];
    }

    public void setOccupancyCell(Point pos, Entity entity) {

        this.occupancy[pos.y][pos.x] = entity;
    }

    public void removeEntityAt(Point pos) {
        if (this.withinBounds(pos) && this.getOccupancyCell(pos) != null) {
            Entity entity = this.getOccupancyCell( pos);

            /* This moves the entity just outside of the grid for
             * debugging purposes. */
            entity.setPosition(new Point(-1, -1));
            this.entities.remove(entity);
            this.setOccupancyCell(pos, null);
        }
    }

    public Optional<Entity> getOccupant(Point pos) {
        if (this.isOccupied(pos)) {
            return Optional.of(this.getOccupancyCell(pos));
        } else {
            return Optional.empty();
        }
    }

    public void moveEntity(EventScheduler scheduler, Entity entity, Point pos) {
        Point oldPos = entity.getPosition();
        if (this.withinBounds(pos) && !pos.equals(oldPos)) {
            this.setOccupancyCell(oldPos, null);
            Optional<Entity> occupant = this.getOccupant(pos);
            occupant.ifPresent(target -> this.removeEntity(scheduler, target));
            this.setOccupancyCell(pos, entity);
            entity.setPosition(pos);
        }
    }
    /*
           Assumes that there is no entity currently occupying the
           intended destination cell.
        */
    public void addEntity(Entity entity) {
        if (this.withinBounds(entity.getPosition())) {
            this.setOccupancyCell(entity.getPosition(), entity);
            this.entities().add(entity);
        }
    }
    public void removeEntity( EventScheduler scheduler, Entity entity) {
        try{
            ActionDoer actDo = (ActionDoer)entity;
            scheduler.unscheduleAllEvents(actDo);
        }catch(ClassCastException exc){

        }
        this.removeEntityAt(entity.getPosition());
    }

    public Optional<Entity> findNearest(Point pos, List<String> entityKeys) {
        List<Entity> listOfEntities = new LinkedList<>();
        for (String key : entityKeys) {
            for (Entity entity : this.entities) {
                if (entity.getKey().equals(key)) {
                    listOfEntities.add(entity);
                }
            }
        }
        return nearestEntity(listOfEntities, pos);
    }
    public Optional<Entity> nearestEntity(List<Entity> entities, Point pos){
        if (entities.isEmpty()) {
            return Optional.empty();
        } else {
            Entity nearest = entities.get(0);
            int nearestDistance = Node.distanceHeuristic(pos, nearest.getPosition());
            //int nearestDistance = pos.distanceSquared(nearest.getPosition());

            for (Entity other : entities) {
                int otherDistance = Node.distanceHeuristic(pos, other.getPosition());
                //int otherDistance = pos.distanceSquared(other.getPosition());

                if (otherDistance < nearestDistance) {
                    nearest = other;
                    nearestDistance = otherDistance;
                }
            }

            return Optional.of(nearest);
        }
    }
    public boolean isOccupied(Point pos) {
        return this.withinBounds(pos) && this.getOccupancyCell(pos) != null;
    }

    public boolean withinBounds(Point pos) {
        return pos.y >= 0 && pos.y < this.numRows &&
                pos.x >= 0 && pos.x < this.numCols;
    }


    public Background getBackgroundCell(Point pos) {
        return this.background[pos.y][pos.x];
    }

    public void setBackgroundCell(Point pos, Background background) {
        this.background[pos.y][pos.x] = background;
    }

    public Optional<PImage> getBackgroundImage( Point pos) {
        if (withinBounds(pos)) {
            return Optional.of((getBackgroundCell(pos).getCurrentImage()));
        } else {
            return Optional.empty();
        }
    }

    public void load(Scanner saveFile, ImageStore imageStore, Background defaultBackground){
        parseSaveFile(saveFile, imageStore, defaultBackground);
        if(this.background == null){
            this.background = new Background[this.numRows][this.numCols];
            for (Background[] row : this.background)
                Arrays.fill(row, defaultBackground);
        }
        if(this.occupancy == null){
            this.occupancy = new Entity[this.numRows][this.numCols];
            this.entities = new HashSet<>();
        }
    }

    public void parseSaveFile(Scanner saveFile, ImageStore imageStore, Background defaultBackground){
        String lastHeader = "";
        int headerLine = 0;
        int lineCounter = 0;
        while(saveFile.hasNextLine()){
            lineCounter++;
            String line = saveFile.nextLine().strip();
            if(line.endsWith(":")){
                headerLine = lineCounter;
                lastHeader = line;
                switch (line){
                    case "Backgrounds:" -> this.background = new Background[this.numRows][this.numCols];
                    case "Entities:" -> {
                        this.occupancy = new Entity[this.numRows][this.numCols];
                        this.entities = new HashSet<>();
                    }
                }
            }else{
                switch (lastHeader){
                    case "Rows:" -> this.numRows = Integer.parseInt(line);
                    case "Cols:" -> this.numCols = Integer.parseInt(line);
                    case "Backgrounds:" -> this.parseBackgroundRow(line, lineCounter-headerLine-1, imageStore);
                    case "Entities:" -> parseEntity(this, line, imageStore);
                }
            }
        }
    }

    public static void parseEntity(WorldModel world, String line, ImageStore imageStore) {
        String[] properties = line.split(" ", Entity.MIN_PROPERTIES + 1);
        if (properties.length >= Entity.MIN_PROPERTIES) {
            String key = properties[Entity.PROPERTY_KEY];
            String id = properties[Entity.PROPERTY_ID];
            Point pt = new Point(Integer.parseInt(properties[Entity.PROPERTY_COL]), Integer.parseInt(properties[Entity.PROPERTY_ROW]));

            properties = properties.length == Entity.MIN_PROPERTIES ?
                    new String[0] : properties[Entity.MIN_PROPERTIES].split(" ");

            switch (key.toUpperCase()) {
                case Obstacle.KIND -> world.parseObstacle(properties, pt, id, imageStore);
                case Dude.KIND -> world.parseDude(properties, pt, id, imageStore);
                case Fairy.KIND -> world.parseFairy(properties, pt, id, imageStore);
                case House.KIND -> world.parseHouse(properties, pt, id, imageStore);
                case Tree.KIND -> world.parseTree(properties, pt, id, imageStore);
                case Sapling.KIND -> world.parseSapling(properties, pt, id, imageStore);
                case Stump.KIND -> world.parseStump(properties, pt, id, imageStore);
                default -> throw new IllegalArgumentException("Entity key is unknown");
            }
        }else{
            throw new IllegalArgumentException("Entity must be formatted as [key] [id] [x] [y] ...");
        }
    }

    public void tryAddEntity(Entity entity) {
        if (isOccupied(entity.getPosition())) {
            // arguably the wrong type of exception, but we are not
            // defining our own exceptions yet
            throw new IllegalArgumentException("position occupied");
        }

        this.addEntity(entity);
    }

    public void parseBackgroundRow(String line, int row, ImageStore imageStore) {
        String[] cells = line.split(" ");
        if(row < this.numRows){
            int rows = Math.min(cells.length, this.numCols);
            for (int col = 0; col < rows; col++){
                this.background[row][col] = new Background(cells[col],
                        imageStore.getImageList(cells[col]));
            }
        }
    }

    public void parseSapling(String[] properties, Point pt, String id, ImageStore imageStore) {
        if (properties.length == Sapling.NUM_PROPERTIES) {
            int health = Integer.parseInt(properties[Sapling.HEALTH_INDEX]);
            Entity entity = new Sapling(id, pt, imageStore.getImageList(Sapling.KIND.toLowerCase()), health);
            this.tryAddEntity(entity);
        }else{
            throw new IllegalArgumentException(String.format("%s requires %d properties when parsing", Sapling.KIND.toLowerCase(), Sapling.NUM_PROPERTIES));
        }
    }

    public void parseDude(String[] properties, Point pt, String id, ImageStore imageStore) {
        if (properties.length == Dude.NUM_PROPERTIES) {
            Entity entity = new DudeNotFull(id, pt, imageStore.getImageList(Dude.KIND.toLowerCase()), Double.parseDouble(properties[Dude.ANIMATION_PERIOD]),
                    Double.parseDouble(properties[Dude.ACTION_PERIOD]), Integer.parseInt(properties[Dude.LIMIT]));
            this.tryAddEntity(entity);
        }else{
            throw new IllegalArgumentException(String.format("%s requires %d properties when parsing", Dude.KIND.toLowerCase(), Dude.NUM_PROPERTIES));
        }
    }

    public void parseFairy(String[] properties, Point pt, String id, ImageStore imageStore) {
        if (properties.length == Fairy.NUM_PROPERTIES) {
            Entity entity = new Fairy(id, pt, imageStore.getImageList(Fairy.KIND.toLowerCase()),
                    Double.parseDouble(properties[Fairy.ANIMATION_PERIOD]), Double.parseDouble(properties[Fairy.ACTION_PERIOD]));
            this.tryAddEntity(entity);
        }else{
            throw new IllegalArgumentException(String.format("%s requires %d properties when parsing", Fairy.KIND.toLowerCase(), Fairy.NUM_PROPERTIES));
        }
    }

    public void parseTree(String[] properties, Point pt, String id, ImageStore imageStore) {
        if (properties.length == Tree.NUM_PROPERTIES) {
            Entity entity = new Tree(id, pt, imageStore.getImageList(Tree.KIND.toLowerCase()), Integer.parseInt(properties[Tree.HEALTH]),
                    Double.parseDouble(properties[Tree.ANIMATION_PERIOD]), Double.parseDouble(properties[Tree.ACTION_PERIOD]));
            this.tryAddEntity(entity);
        }else{
            throw new IllegalArgumentException(String.format("%s requires %d properties when parsing", Tree.KIND.toLowerCase(), Tree.NUM_PROPERTIES));
        }
    }

    public void parseObstacle(String[] properties, Point pt, String id, ImageStore imageStore) {
        if (properties.length == Obstacle.NUM_PROPERTIES) {
            Entity entity = new Obstacle(id, pt, imageStore.getImageList(Obstacle.KIND.toLowerCase()),
                    Double.parseDouble(properties[Obstacle.ANIMATION_PERIOD]));
            this.tryAddEntity(entity);
        }else{
            throw new IllegalArgumentException(String.format("%s requires %d properties when parsing", Obstacle.KIND.toLowerCase(), Obstacle.NUM_PROPERTIES));
        }
    }

    public void parseHouse(String[] properties, Point pt, String id, ImageStore imageStore) {
        if (properties.length == House.NUM_PROPERTIES) {
            Entity entity = new House(id, pt, imageStore.getImageList(House.KIND.toLowerCase()));
            this.tryAddEntity(entity);
        }else{
            throw new IllegalArgumentException(String.format("%s requires %d properties when parsing", House.KIND.toLowerCase(), House.NUM_PROPERTIES));
        }
    }

    public void parseStump(String[] properties, Point pt, String id, ImageStore imageStore) {
        if (properties.length == Stump.NUM_PROPERTIES) {
            Entity entity = new Stump(id, pt, imageStore.getImageList(Stump.KIND.toLowerCase()));
            this.tryAddEntity(entity);
        }else{
            throw new IllegalArgumentException(String.format("%s requires %d properties when parsing", Stump.KIND.toLowerCase(), Stump.NUM_PROPERTIES));
        }
    }

    /**
     * Helper method for testing. Don't move or modify this method.
     */
    public List<String> log(){
        List<String> list = new ArrayList<>();
        for (Entity entity : entities) {
            String log = entity.log();
            if(log != null) list.add(log);
        }
        return list;
    }
}
