import processing.core.PImage;

import java.util.List;
import java.util.function.BiPredicate;

public abstract class Dude extends Mover implements Transform, ClickEventTransform, WizardTransform {

    public static final int NUM_PROPERTIES = 3;
    public static final int ACTION_PERIOD = 0;
    public static final int ANIMATION_PERIOD = 1;
    public static final int LIMIT = 2;
    public static final String KIND = "DUDE";
    private final String KEY = KIND.toLowerCase();
    //private static final PathingStrategy Dude_PATHING = new SingleStepPathingStrategy();
    private static final PathingStrategy Dude_PATHING = new AStarPathingStrategy();

    private int resourceLimit;
    public Dude(String id, Point position, List<PImage> images,
                 double animationPeriod, double actionPeriod, int resourceLimit){
        super(id, position, images, animationPeriod, actionPeriod,Dude_PATHING);
        this.resourceLimit = resourceLimit;
    }

    @Override
    public Point nextPosition(WorldModel world, Point destPos) {
        BiPredicate<Point, Point> withinReach =
                (curPos, desPos) -> {
                    if (curPos.adjacent(desPos))
                        return true;
                    return false;
                };

        List<Point> path = Dude_PATHING.computePath(
                getPosition(), // start Point
                destPos, // end Point
                //p -> world.withinBounds(p) && (!world.isOccupied(p) || world.getOccupancyCell(p).getKey().equals(Stump.KIND.toLowerCase())), //canPassTrough
                p -> world.withinBounds(p) && (!world.isOccupied(p)), //canPassTrough
                Node::neighbors, //withinReach
                PathingStrategy.CARDINAL_NEIGHBORS);
                //PathingStrategy.DIAGONAL_CARDINAL_NEIGHBORS);
        if (path.size() == 0) {
            return this.getPosition();
        }else{
            return path.get(0);
        }
    }
    /*@Override
    public Point nextPosition(WorldModel world, Point destPos) {
        int horiz = Integer.signum(destPos.x - this.getPosition().x);
        Point newPos = new Point(this.getPosition().x + horiz, this.getPosition().y);
        if (horiz == 0 || world.isOccupied(newPos) && !(world.getOccupancyCell(newPos).getKey().equals(Stump.KIND.toLowerCase()))){
        //if (horiz == 0 || world.isOccupied(newPos)){
            int vert = Integer.signum(destPos.y - this.getPosition().y);
            newPos = new Point(this.getPosition().x, this.getPosition().y + vert);

            if (vert == 0 || world.isOccupied(newPos) && !(world.getOccupancyCell(newPos).getKey().equals(Stump.KIND.toLowerCase()))) {
                newPos = this.getPosition();
            }
        }

        return newPos;
    }*/

    public int getResourceLimit() { return resourceLimit; }
    public String getKey(){
        return this.KEY;
    }
    public boolean clickTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity skeleton = new Skeleton(Skeleton.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(Skeleton.KIND.toLowerCase()), 0.2, 0.85);
        world.removeEntity( scheduler,this);
        world.addEntity(skeleton);
        ((ActionDoer)skeleton).scheduleActions(scheduler, world, imageStore);
        //EntityTransformer.transformToSkeleton(world, scheduler, imageStore, this);
        return true;
    }

    @Override
    public boolean wizardTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity bigmush = new BigMushroom(BigMushroom.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(BigMushroom.KIND.toLowerCase()));
        world.removeEntity( scheduler,this);
        world.addEntity(bigmush);
        //EntityTransformer.transformToBigMushroom(world, scheduler, imageStore, this);
        return true;

    }
}
