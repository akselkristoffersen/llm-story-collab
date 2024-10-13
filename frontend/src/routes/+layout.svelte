<script>
    import 'modern-normalize/modern-normalize.css';
    import '../styles/main.scss';
</script>

<main id="main-content">
    <slot />
</main>

<style lang="scss">
    #main-content {
        width: 100vw;
        height: 100vh;
        height: 100dvh;
        display: flex;
        justify-content: center;
    }
</style>