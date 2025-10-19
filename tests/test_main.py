import runpy


def test_main():
    import main

    main.main()
    runpy.run_module("main", run_name="__main__")
