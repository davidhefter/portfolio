public abstract class Action {
    private ActionDoer actionDoer;
    public Action(ActionDoer actionDoer){
        this.actionDoer = actionDoer;
    }
    public abstract void executeAction(EventScheduler scheduler);
    public ActionDoer getActionDoer(){ return this.actionDoer; }
}
