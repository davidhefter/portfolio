/**
 * An event is made up of an Original.Entity that is taking an
 * Original.Action a specified time.
 */
public final class Event {
    private Action action;
    private double time;
    private ActionDoer actionDoer;

    public Event(Action action, double time, ActionDoer actionDoer) {
        this.action = action;
        this.time = time;
        this.actionDoer = actionDoer;
    }
    public Action action(){return this.action;}
    public double time(){return this.time;}
    public ActionDoer actionDoer(){return this.actionDoer;}
}
