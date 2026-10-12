def simulate_service():
    try:
        line1 = input().split()
        if not line1: return
        n = int(line1[0]) # Number of customers [cite: 37]
        
        current_time = 0
        total_waiting_time = 0
        results = []

        for i in range(1, n + 1):
            # Ai = Arrival time, Si = Service time [cite: 29, 30, 38]
            a_i, s_i = map(int, input().split())
            
            # Start time is the maximum of arrival time or when the counter is free [cite: 31]
            start_time = max(a_i, current_time)
            finish_time = start_time + s_i
            
            wait_time = start_time - a_i
            total_waiting_time += wait_time
            
            results.append(f"Customer {i}: start={start_time} finish={finish_time}")
            current_time = finish_time

        for res in results:
            print(res)
        print(f"TotalWaitingTime={total_waiting_time}") # [cite: 44]
        
    except EOFError:
        pass

if __name__ == "__main__":
    simulate_service()