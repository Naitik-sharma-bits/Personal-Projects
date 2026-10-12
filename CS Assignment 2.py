import sys as s
import threading as th

log_lock = th.Lock()

def log_action(name, action):
    """Logs an action to the console safely."""
    with log_lock:
        print(f"[{name}]: {action}")


class Meetingcordinator:

    def __init__(self, k):
        #for all conditions and rules
        self.K = k

        self.students_in_chamber = 0
        self.staff_in_chamber = 0
        self.online_meeting_active = False

        self.students_waiting = 0
        self.staff_waiting = 0
        self.online_meetings_waiting = 0

        self.chamber_full_s = False
        self.chamber_full_a = False

        self.lock = th.Lock()
        
        self.cond_student = th.Condition(self.lock)
        self.cond_staff = th.Condition(self.lock)
        self.cond_online = th.Condition(self.lock)

    def student_enter(self, name):
        """Protocol for a student to enter the chamber."""
        with self.lock:
            self.students_waiting += 1
            wait_condition = lambda: (
                self.staff_in_chamber > 0 or
                self.online_meeting_active or
                self.online_meetings_waiting > 0 or
                self.chamber_full_s
            )
            self.cond_student.wait_for(lambda: not wait_condition())
            self.students_waiting -= 1
            self.students_in_chamber += 1

            log_action(name, f"enters chamber. (Students: {self.students_in_chamber}/{self.K})")
            
            if self.students_in_chamber == self.K:
                self.chamber_full_s = True

    def student_leave(self, name):
        """Protocol for a student to leave the chamber."""
        with self.lock:
            self.students_in_chamber -= 1

            log_action(name, f"leaves chamber. (Students: {self.students_in_chamber}/{self.K})")

            if self.students_in_chamber == 0:
                self.chamber_full_s = False

                if self.online_meetings_waiting > 0:
                    self.cond_online.notify() 
                elif self.staff_waiting > 0:
                    self.cond_staff.notify_all() 
                else:
                    self.cond_student.notify_all() 

    def staff_enter(self, name):
        """Protocol for administrative staff to enter the chamber."""
        with self.lock:
            self.staff_waiting += 1

            wait_condition = lambda: (
                self.students_in_chamber > 0 or
                self.online_meeting_active or
                self.online_meetings_waiting > 0 or
                self.chamber_full_a
            )
            
            self.cond_staff.wait_for(lambda: not wait_condition())
            self.staff_waiting -= 1
            self.staff_in_chamber += 1

            log_action(name, f"enters chamber. (Staff: {self.staff_in_chamber}/{self.K})")

            if self.staff_in_chamber == self.K:
                self.chamber_full_a = True

    def staff_leave(self, name):
        """Protocol for administrative staff to leave the chamber."""
        with self.lock:
            self.staff_in_chamber -= 1

            log_action(name, f"leaves chamber. (Staff: {self.staff_in_chamber}/{self.K})")

            if self.staff_in_chamber == 0:
                self.chamber_full_a = False

                if self.online_meetings_waiting > 0:
                    self.cond_online.notify()
                elif self.students_waiting > 0:
                    self.cond_student.notify_all()
                else:
                    self.cond_staff.notify_all()

    def online_enter(self, name):
        """Protocol for an online meeting to start."""
        with self.lock:
            self.online_meetings_waiting += 1

            wait_condition = lambda: (
                self.students_in_chamber > 0 or
                self.staff_in_chamber > 0 or
                self.online_meeting_active
            )
            
            self.cond_online.wait_for(lambda: not wait_condition())

            self.online_meetings_waiting -= 1
            self.online_meeting_active = True

            log_action(name, "enters chamber. (Online meeting started)")

    def online_leave(self, name):
        """Protocol for an online meeting to end."""
        with self.lock:
            self.online_meeting_active = False

            log_action(name, "leaves chamber. (Online meeting finished)")

            if self.online_meetings_waiting > 0:
                self.cond_online.notify()
            elif self.students_waiting > 0:
                self.cond_student.notify_all()
            elif self.staff_waiting > 0:
                self.cond_staff.notify_all()

#Thread Target Functions 

def student_thread(name, monitor):
    """Main function for a student thread."""
    log_action(name, "arrives at chamber.")
    monitor.student_enter(name)
    log_action(name, "is meeting with the professor.")

    monitor.student_leave(name)

def staff_thread(name, monitor):
    """Main function for a staff thread."""
    log_action(name, "arrives at chamber.")
    monitor.staff_enter(name)
    log_action(name, "is meeting with the professor.")

    monitor.staff_leave(name)

def online_thread(name, monitor):
    """Main function for an online meeting thread."""
    log_action(name, "arrives (online meeting request).")
    monitor.online_enter(name)
    log_action(name, "is in progress.")

    monitor.online_leave(name)

##Main##

def main():
    try:
        K = int(input("Enter the no. of chairs:"))
        if K <= 0:
            raise ValueError()
    except ValueError:
        print("Error: K must be a positive integer.", file=s.stderr)
        s.exit(1)

    try:
        infile = open("MeetingInfo.txt", "r")
    except FileNotFoundError:
        print("Error: Cannot open MeetingInfo.txt", file=s.stderr)
        s.exit(1)

    print(f"Professor's chamber has {K} chairs.")

    monitor = Meetingcordinator(K)
    threads = []

    for line in infile:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        if len(parts) != 2:
            print(f"Warning: Skipping malformed line: {line}", file=s.stderr)
            continue

        name, type = parts

        if type == 'S':
            target_func = student_thread
        elif type == 'A':
            target_func = staff_thread
        elif type == 'O':
            target_func = online_thread
        else:
            print(f"Warning: Skipping unknown type: {type}", file=s.stderr)
            continue
        
        t = th.Thread(target=target_func, args=(name, monitor))
        threads.append(t)
        t.start()

    infile.close()

    print("--- All visitors have arrived. Waiting for meetings to finish... ---")

    for t in threads:
        t.join()

    print("All meetings are finished. Professor is going home.")

if __name__ == "__main__":
    main()