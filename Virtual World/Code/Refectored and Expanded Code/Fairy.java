import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;

public class Fairy extends Mover implements WizardTransform, ClickEventTransform, SkeletonTransform{
    public static final String KIND = "FAIRY";
    public static final int NUM_PROPERTIES = 2;
    public static final int ANIMATION_PERIOD = 0;
    public static final int ACTION_PERIOD = 1;
    private final String KEY = KIND.toLowerCase();
    private Entity currentTarget;
    //private static final PathingStrategy Fairy_PATHING = new SingleStepPathingStrategy();
    private static final PathingStrategy Fairy_PATHING = new AStarPathingStrategy();

    public Fairy(String id, Point position, List<PImage> images,
                 double animationPeriod, double actionPeriod){
        super(id, position, images, animationPeriod, actionPeriod,Fairy_PATHING);
    }

    @Override
    public void executeActivity(WorldModel world, ImageStore imageStore, EventScheduler scheduler) {
        Optional<Entity> fairyTarget = world.findNearest(this.getPosition(),
                new ArrayList<>(List.of(Skeleton.KIND.toLowerCase(), BigMushroom.KIND.toLowerCase())));
        if (!fairyTarget.isPresent()){
            fairyTarget = world.findNearest(this.getPosition(),
                    new ArrayList<>(List.of(Stump.KIND.toLowerCase())));
        }
        if (fairyTarget.isPresent()) {
            Point tgtPos = fairyTarget.get().getPosition();

            if (moveTo( world, fairyTarget.get(), scheduler)) {
                ((FairyTransform)(fairyTarget.get())).fairyTransform(world, scheduler, imageStore);
            }
        }

        scheduler.scheduleEvent(this, new Activity(this, world, imageStore), this.getActionPeriod());

        if (world.getBackgroundCell(this.getPosition()).getImageID().equals("mushrooms")){
            if(Math.random()>0.5){
                world.setBackgroundCell(this.getPosition(), new Background("grass", imageStore.getImageList("grass")));
            }else{
                world.setBackgroundCell(this.getPosition(), new Background("flowers", imageStore.getImageList("flowers")));
            }
        }
    }

    @Override
    public boolean moveTo(WorldModel world, Entity target, EventScheduler scheduler) {
        /*if (this.currentTarget==null
                || (world.getOccupant(this.currentTarget.getPosition()).isPresent() &&
                !world.getOccupant(this.currentTarget.getPosition()).get().getKey().equals("stump"))){
            this.currentTarget = target;
            System.out.println("fairy");
        }*/

        //if (this.getPosition().adjacent(this.currentTarget.getPosition())) {
        if (this.getPosition().adjacent(target.getPosition())) {
            //world.removeEntity( scheduler,this.currentTarget);

            //world.removeEntity( scheduler,target);
            //this.currentTarget = null;
            return true;
        } else {
            //Point nextPos = nextPosition(world, this.currentTarget.getPosition());
            Point nextPos = nextPosition(world, target.getPosition());

            if (!this.getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }
            return false;
        }
    }
    @Override
    public Point nextPosition(WorldModel world, Point destPos) {
        BiPredicate<Point, Point> withinReach =
                (curPos, desPos) -> {
                    if (curPos.adjacent(desPos))
                        return true;
                    return false;
                };

        List<Point> path = Fairy_PATHING.computePath(
                getPosition(), // start Point
                destPos, // end Point
                p -> world.withinBounds(p) && !world.isOccupied(p), //canPassTrough
                Node::neighbors, //withinReach
                //PathingStrategy.CARDINAL_NEIGHBORS);
                PathingStrategy.DIAGONAL_CARDINAL_NEIGHBORS);
        if (path.size() == 0) {
            return this.getPosition();
        }
        else {
            return path.get(0);
        }
    }
    /*@Override
    public Point nextPosition(WorldModel world, Point destPos) {
        int horiz = Integer.signum(destPos.x - this.getPosition().x);
        Point newPos = new Point(this.getPosition().x + horiz, this.getPosition().y);

        if (horiz == 0 || world.isOccupied(newPos)) {
            int vert = Integer.signum(destPos.y - this.getPosition().y);
            newPos = new Point(this.getPosition().x, this.getPosition().y + vert);

            if (vert == 0 || world.isOccupied(newPos)) {
                newPos = this.getPosition();
            }
        }
        return newPos;
    }*/
    @Override
    public String getKey(){
        return KEY;
    }
    @Override
    public boolean wizardTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity skeleton = new Skeleton(Skeleton.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(Skeleton.KIND.toLowerCase()), 0.2, 0.85);
        world.removeEntity( scheduler,this);
        world.addEntity(skeleton);
        ((ActionDoer)skeleton).scheduleActions(scheduler, world, imageStore);
        //EntityTransformer.transformToSkeleton(world, scheduler, imageStore, this);
        return true;
    }
    @Override
    public boolean clickTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore) {
        Entity wizard = new Wizard(Wizard.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(Wizard.KIND.toLowerCase()), 0.2, 0.5);
        world.removeEntity( scheduler,this);
        world.addEntity(wizard);
        ((ActionDoer)wizard).scheduleActions(scheduler, world, imageStore);
        //EntityTransformer.transformToWizard(world, scheduler, imageStore, this);
        return true;
    }
    @Override
    public boolean skeletonTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore) {
        Entity bigmush = new BigMushroom(BigMushroom.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(BigMushroom.KIND.toLowerCase()));
        world.removeEntity( scheduler,this);
        world.addEntity(bigmush);
        //EntityTransformer.transformToBigMushroom(world, scheduler, imageStore, this);
        return true;
    }
}
