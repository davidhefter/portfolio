//THIS WAS UNUSED DUE TO PERFORMANCE ISSUES

public class EntityTransformer {
    public static void transformToWizard(WorldModel world, EventScheduler scheduler, ImageStore imageStore, Entity entity){
        Entity wizard = new Wizard(Wizard.KIND.toLowerCase() + "_" + entity.getId(), entity.getPosition(), imageStore.getImageList(Wizard.KIND.toLowerCase()), 0.2, 0.5);
        world.removeEntity( scheduler,entity);
        world.addEntity(wizard);
        ((ActionDoer)wizard).scheduleActions(scheduler, world, imageStore);
    }

    public static void transformToBigMushroom(WorldModel world, EventScheduler scheduler, ImageStore imageStore, Entity entity){
        Entity bigmush = new BigMushroom(BigMushroom.KIND.toLowerCase() + "_" + entity.getId(), entity.getPosition(), imageStore.getImageList(BigMushroom.KIND.toLowerCase()));
        world.removeEntity( scheduler,entity);
        world.addEntity(bigmush);
    }

    public static void transformToSkeleton(WorldModel world, EventScheduler scheduler, ImageStore imageStore, Entity entity){
        Entity skeleton = new Skeleton(Skeleton.KIND.toLowerCase() + "_" + entity.getId(), entity.getPosition(), imageStore.getImageList(Skeleton.KIND.toLowerCase()), 0.2, 0.85);
        world.removeEntity( scheduler,entity);
        world.addEntity(skeleton);
        ((ActionDoer)skeleton).scheduleActions(scheduler, world, imageStore);
    }
    public static void transformToDudeNotFull(WorldModel world, EventScheduler scheduler, ImageStore imageStore, Entity entity) {
        Entity dude = new DudeNotFull(entity.getId(), entity.getPosition(), imageStore.getImageList(Dude.KIND.toLowerCase()), (Math.random() * .1) + .7,
                0.18, 5);
        world.removeEntity(scheduler, entity);
        world.addEntity(dude);
        ((ActionDoer) dude).scheduleActions(scheduler, world, imageStore);
    }
    public static void transformToSapling(WorldModel world, EventScheduler scheduler, ImageStore imageStore, Entity entity){
        Entity sapling = new Sapling(Sapling.KIND.toLowerCase() + "_" + entity.getId(), entity.getPosition(),
                imageStore.getImageList(Sapling.KIND.toLowerCase()), 0);
        world.removeEntity(scheduler, entity);
        world.addEntity(sapling);
        ((ActionDoer)sapling).scheduleActions(scheduler, world, imageStore);
    }

    public static void transformToFairy(WorldModel world, EventScheduler scheduler, ImageStore imageStore, Entity entity){
        Entity fairy = new Fairy(Fairy.KIND.toLowerCase() + "_" + entity.getId(), entity.getPosition(), imageStore.getImageList(Fairy.KIND.toLowerCase()), 0.15, 0.15);
        world.removeEntity( scheduler,entity);
        world.addEntity(fairy);
        ((ActionDoer)fairy).scheduleActions(scheduler, world, imageStore);
    }

    public static void transformToStump(WorldModel world, EventScheduler scheduler, ImageStore imageStore, Entity entity){
        Entity stump = new Stump(Stump.KIND.toLowerCase() + "_" + entity.getId(), entity.getPosition(), imageStore.getImageList(Stump.KIND.toLowerCase()));
        world.removeEntity( scheduler,entity);
        world.addEntity(stump);
    }
}
