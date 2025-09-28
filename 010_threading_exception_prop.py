import threading


# =====================================
# shows that exception raised in thread
# do not propagate into main
# =====================================


def task_that_fail(tastk_id, should_fail=True):
    print(f"Task {tastk_id} starting ...")

    if should_fail:
        raise ValueError(f"Task {tastk_id} failing ...")
    
    print(f"Task {tastk_id} completed successfully")


def main():

    t1 = threading.Thread(target=task_that_fail, args=(1, False))
    t2 = threading.Thread(target=task_that_fail, args=(2, True))
    t1.start()
    t2.start()
    t2.join()

    print("Main completed without exception")


if __name__ == '__main__':
    main()
    