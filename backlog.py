'''
1. Add visualization
'''
import collections
import math

import visualize
import job_definition

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model


def MinimalJobshopSat(jobs_data, jobs_type):
    """Minimal jobshop problem."""
    # Create the model.
    model = cp_model.CpModel()

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)

    # Computes horizon dynamically as the sum of all durations.
    horizon = math.ceil(sum(task[1] for job in jobs_data for task in job))

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval type')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)
    type_to_intervals = collections.defaultdict(list)

    for i in range(len(jobs_data)):
        job = jobs_data[i]

        for task_id, task in enumerate(job):
            machine = task[0]
            duration = math.ceil(task[1])
            suffix = '_%i_%i' % (i, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[i, task_id] = task_type(start=start_var,
                                                   end=end_var,
                                                   interval=interval_var,
                                                   type = jobs_type[i])
            machine_to_intervals[machine].append(interval_var)
            type_to_intervals[jobs_type[i]].append(interval_var)


    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    for i in range(len(type_to_intervals.keys())): 
        intervals = type_to_intervals[i]
        model.AddCumulative(intervals, [1]*len(intervals), 2)

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(start=solver.Value(
                        all_tasks[job_id, task_id].start),
                                       job=job_id,
                                       index=task_id,
                                       duration=task[1]))

        # Create per machine output lines.
        ### Austin
        # Create visualization
        endpoint_times = []
        output = ''
        for i in range(len(all_machines)):
            machine = all_machines[i]
            endpoints = []
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = 'Machine ' + str(machine) + ': '
            sol_line = '           '

            for assigned_task in assigned_jobs[machine]:
                name = 'job_%i_%i' % (assigned_task.job, assigned_task.index)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-10s' % name

                start = assigned_task.start
                duration = assigned_task.duration
                endpoints.append([all_tasks[assigned_task.job, assigned_task.index].type,start, duration])
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-10s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

            endpoint_times.append(endpoints)

        # Finally print the solution found.
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        # print(output)

        # # vis
        # print(endpoint_times)
        visualize.creat_vis(endpoint_times, solver.ObjectiveValue())



test_pass_order = 1

if test_pass_order <= 0:
    current_backlog = {
        # "C17": 34,
        # "E26": 14,
        # "D20": 15,
        # "B15": 58,
        # "D25": 40,
        # "F35": 3,
        "C17": 5,
        "E26": 1,
        "D20": 1,
        "B15": 1,
        "D25": 1,
        "F35": 1,
    }

else:
    job_count = job_definition.past_orders[test_pass_order-1]
    current_backlog = {
        "C17": job_count[0],
        "E26": job_count[1],
        "D20": job_count[2],
        "B15": job_count[3],
        "D25": job_count[4],
        "F35": job_count[5],
    }


jobs_data = []
jobs_type = [] # records the type(E25,F35, ..) of each job in index ^

for i in range(len(job_definition.all_jobs)):
    job_name = job_definition.all_jobs[i]
    job_detail = job_definition.get_job_def(job_name)

    for j in range(current_backlog[job_name]):
        jobs_data.append(job_detail)
        jobs_type.append(i)

# print(jobs_type)

MinimalJobshopSat(jobs_data, jobs_type)