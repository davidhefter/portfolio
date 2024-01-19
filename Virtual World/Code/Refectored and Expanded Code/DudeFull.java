import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class DudeFull extends Dude{
    private Entity currentTarget;
    public DudeFull(String id, Point position, List<PImage> images,
                double animationPeriod, double actionPeriod, int resourceLimit){
        super(id, position, images, animationPeriod, actionPeriod, resourceLimit);
    }
    @Override
    public void executeActivity(WorldModel world, ImageStore imageStore, EventScheduler scheduler) {
        Optional<Entity> fullTarget = world.findNearest(this.getPosition(),
                new ArrayList<>(List.of(House.KIND.toLowerCase(), BigMushroom.KIND.toLowerCase(), Wizard.KIND.toLowerCase())));

        if (fullTarget.isPresent() && moveTo(world, fullTarget.get(), scheduler)) {
            if(fullTarget.get() instanceof House){
                this.transform(world, scheduler, imageStore);
            }else{
                ((DudeTransform)(fullTarget.get())).dudeTransform(world, scheduler, imageStore);
            }
        } else {
            scheduler.scheduleEvent( this, new Activity(this, world, imageStore), this.getActionPeriod());
        }
    }
    @Override
    public boolean moveTo(WorldModel world, Entity target, EventScheduler scheduler) {
        /*if (this.currentTarget==null
                || (world.getOccupant(this.currentTarget.getPosition()).isPresent() &&
                    !world.getOccupant(this.currentTarget.getPosition()).get().getKey().equals("house"))){
            this.currentTarget = target;
            System.out.println("dudefull");
        }*/

        //if (this.getPosition().adjacent(this.currentTarget.getPosition())) {
        if (this.getPosition().adjacent(target.getPosition())) {
            //this.currentTarget = null;
            return true;
        } else {
            //Point nextPos = nextPosition( world, this.currentTarget.getPosition());
            Point nextPos = nextPosition( world, target.getPosition());

            if (!this.getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }
            return false;
        }
    }

    @Override
    public boolean transform(WorldModel world, EventScheduler scheduler, ImageStore imageStore) {
        Entity dude = new DudeNotFull(this.getId(), this.getPosition(), this.getImages(), this.getAnimationPeriod(),
            this.getActionPeriod(), this.getResourceLimit());

        world.removeEntity(scheduler, this);

        world.addEntity(dude);
        ((ActionDoer)dude).scheduleActions(scheduler, world, imageStore);
        return true;
    }

}
