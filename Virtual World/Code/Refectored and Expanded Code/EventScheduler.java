import java.util.*;

/**
 * Keeps track of events that have been scheduled.
 */
public final class EventScheduler {
    private PriorityQueue<Event> eventQueue;
    private Map<ActionDoer, List<Event>> pendingEvents;
    private double currentTime;

    public EventScheduler() {
        this.eventQueue = new PriorityQueue<>(new EventComparator());
        this.pendingEvents = new HashMap<>();
        this.currentTime = 0;
    }
    public double currentTime(){return this.currentTime;}
    public void removePendingEvent(Event event) {
        List<Event> pending = this.pendingEvents.get(event.actionDoer());

        if (pending != null) {
            pending.remove(event);
        }
    }

    public void updateOnTime(double time) {
        double stopTime = this.currentTime + time;
        while (!this.eventQueue.isEmpty() && this.eventQueue.peek().time() <= stopTime) {
            Event next = this.eventQueue.poll();
            removePendingEvent( next);
            this.currentTime = next.time();
            next.action().executeAction( this);
        }
        this.currentTime = stopTime;
    }

    public void unscheduleAllEvents( ActionDoer a) {
        List<Event> pending = this.pendingEvents.remove(a);

        if (pending != null) {
            for (Event event : pending) {
                this.eventQueue.remove(event);
            }
        }
    }

    public void scheduleEvent(ActionDoer actionDoer, Action action, double afterPeriod) {
        double time = this.currentTime + afterPeriod;

        Event event = new Event(action, time, actionDoer);

        this.eventQueue.add(event);

        // update list of pending events for the given actionDoer
        List<Event> pending = this.pendingEvents.getOrDefault(actionDoer, new LinkedList<>());
        pending.add(event);
        this.pendingEvents.put(actionDoer, pending);
    }
}
