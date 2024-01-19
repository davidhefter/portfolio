public class Activity extends Action{
    private WorldModel world;
    private ImageStore imageStore;
    public Activity(ActionDoer actionDoer, WorldModel world, ImageStore imageStore){
        super(actionDoer);
        this.world = world;
        this.imageStore = imageStore;
    }
    public void executeAction(EventScheduler scheduler){
        executeActivity(scheduler);
    }
    public void executeActivity(EventScheduler scheduler){
        try {
            ((Act)this.getActionDoer()).executeActivity(world, imageStore, scheduler);
        }catch (ClassCastException exc){
            System.out.printf("executeActivity not supported for %s",this.getActionDoer().getKey());
        }
    }
}
