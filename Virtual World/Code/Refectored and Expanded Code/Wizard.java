import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;

public class Wizard extends Mover implements ClickEventTransform, DudeTransform{
    public static final String KIND = "WIZARD";
    public static final int NUM_PROPERTIES = 2;
    public static final int ANIMATION_PERIOD = 0;
    public static final int ACTION_PERIOD = 1;
    private final String KEY = KIND.toLowerCase();
    private Entity currentTarget;
    //private static final PathingStrategy Wizard_PATHING = new SingleStepPathingStrategy();
    private static final PathingStrategy Wizard_PATHING = new AStarPathingStrategy();

    public Wizard(String id, Point position, List<PImage> images,
                 double animationPeriod, double actionPeriod){
        super(id, position, images, animationPeriod, actionPeriod,Wizard_PATHING);
    }

    @Override
    public void executeActivity(WorldModel world, ImageStore imageStore, EventScheduler scheduler) {
        Optional<Entity> wizardTarget = world.findNearest(this.getPosition(),
                //, Fairy.KIND.toLowerCase()
                new ArrayList<>(List.of(Dude.KIND.toLowerCase(), Stump.KIND.toLowerCase(), Tree.KIND.toLowerCase(), Sapling.KIND.toLowerCase())));

        if (wizardTarget.isPresent()) {
            Point tgtPos = wizardTarget.get().getPosition();

            if (moveTo( world, wizardTarget.get(), scheduler)) {
                ((WizardTransform)(wizardTarget.get())).wizardTransform(world, scheduler, imageStore);
            }
        }

        scheduler.scheduleEvent(this, new Activity(this, world, imageStore), this.getActionPeriod());
        if (world.getBackgroundCell(this.getPosition()).getImageID().equals("grass") || world.getBackgroundCell(this.getPosition()).getImageID().equals("flowers")){
            world.setBackgroundCell(this.getPosition(), new Background("mushrooms", imageStore.getImageList("mushrooms")));
        }
    }

    @Override
    public boolean moveTo(WorldModel world, Entity target, EventScheduler scheduler) {
        /*if (this.currentTarget==null
                || (world.getOccupant(this.currentTarget.getPosition()).isPresent() &&
                !world.getOccupant(this.currentTarget.getPosition()).get().getKey().equals("stump"))){
            this.currentTarget = target;
            System.out.println("wizard");
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

        List<Point> path = Wizard_PATHING.computePath(
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
    public boolean clickTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity dude = new DudeNotFull(this.getId(), this.getPosition(), imageStore.getImageList(Dude.KIND.toLowerCase()), (Math.random() * .1) + .7,
                0.18, 5);
        world.removeEntity(scheduler, this);
        world.addEntity(dude);
        ((ActionDoer)dude).scheduleActions(scheduler, world, imageStore);
        //EntityTransformer.transformToDudeNotFull(world, scheduler, imageStore, this);
        return true;
    }
    @Override
    public boolean dudeTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity stump = new Stump(Stump.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(Stump.KIND.toLowerCase()));
        world.removeEntity( scheduler,this);
        world.addEntity(stump);
        //EntityTransformer.transformToStump(world, scheduler, imageStore, this);
        return true;
    }

}
