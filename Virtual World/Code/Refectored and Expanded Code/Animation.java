public class Animation extends Action{
    private int repeatCount;
    public Animation(ActionDoer actionDoer, int repeatCount){
        super(actionDoer);
        this.repeatCount = repeatCount;
    }
    public void executeAction(EventScheduler scheduler){
        executeAnimation(scheduler);
    }

    public void executeAnimation(EventScheduler scheduler){
        try {
            ((Animate)this.getActionDoer()).nextImage();
            if (this.repeatCount != 1) {
                scheduler.scheduleEvent(this.getActionDoer(),
                        new Animation(this.getActionDoer(),
                                Math.max(this.repeatCount - 1, 0)),
                        ((Animate)this.getActionDoer()).getAnimationPeriod());
            }
        }catch (ClassCastException exc){
            System.out.printf("executeAnimation not supported for %s",this.getActionDoer().getKey());
        }
    }
}
