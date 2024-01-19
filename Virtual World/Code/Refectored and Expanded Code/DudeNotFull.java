import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class DudeNotFull extends Dude{
    private int resourceCount;
    private Entity currentTarget;
    public DudeNotFull(String id, Point position, List<PImage> images,
                    double animationPeriod, double actionPeriod, int resourceLimit){
        super(id, position, images, animationPeriod, actionPeriod, resourceLimit);
        this.resourceCount = 0;
    }

    @Override
    public void executeActivity(WorldModel world, ImageStore imageStore, EventScheduler scheduler) {
        Optional<Entity> target = world.findNearest(this.getPosition(),
                new ArrayList<>(List.of(Tree.KIND.toLowerCase(), Sapling.KIND.toLowerCase(), BigMushroom.KIND.toLowerCase(), Wizard.KIND.toLowerCase())));

        /*if (target.isPresent()) {

            if (moveTo( world, target.get(), scheduler)) {
                ((DudeTransform)(target.get())).dudeTransform(world, scheduler, imageStore);
            }
        }else {
            scheduler.scheduleEvent(this, new Activity(this, world, imageStore), this.getActionPeriod());
        }*/
        if (target.isEmpty() || !moveTo(world, target.get(), scheduler) || !this.transform(world, scheduler, imageStore)) {
            scheduler.scheduleEvent(this, new Activity(this, world, imageStore), this.getActionPeriod());
        }else{
            if (target.isPresent()) {

                if (moveTo(world, target.get(), scheduler)) {
                    ((DudeTransform) (target.get())).dudeTransform(world, scheduler, imageStore);
                }
            }
        }
    }
    @Override
    public boolean moveTo(WorldModel world, Entity target, EventScheduler scheduler) {
        /*if (this.currentTarget==null
                || (world.getOccupant(this.currentTarget.getPosition()).isPresent() &&
                    !(world.getOccupant(this.currentTarget.getPosition()).get().getKey().equals("tree") ||
                        world.getOccupant(this.currentTarget.getPosition()).get().getKey().equals("sapling")))){
            this.currentTarget = target;
            System.out.println("dudenotfull");
        }*/

        //Plant targ = (Plant)this.currentTarget;
        if (this.getPosition().adjacent(target.getPosition())) {
            if(target instanceof Plant){
                Plant targ = (Plant)target;
                this.resourceCount += 1;
                targ.decrementHealth();
            }
            //this.currentTarget = null;
            return true;
        } else {
            Point nextPos = nextPosition(world, target.getPosition());

            if (!this.getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }
            return false;
        }
    }

    @Override
    public boolean transform(WorldModel world, EventScheduler scheduler, ImageStore imageStore) {
        if (this.resourceCount >= this.getResourceLimit()) {
            Entity dude = new DudeFull(this.getId(), this.getPosition(), this.getImages(), this.getAnimationPeriod(),
                    this.getActionPeriod(), this.getResourceLimit());

            world.removeEntity(scheduler, this);
            scheduler.unscheduleAllEvents(this);

            world.addEntity(dude);
            ((ActionDoer)dude).scheduleActions(scheduler, world, imageStore);

            return true;
        }

        return false;
    }

}
