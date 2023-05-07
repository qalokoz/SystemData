public class RefreshableScope extends SimpleThreadScope {

    private boolean refreshed = false;

    @Override
    public void start() {
        super.start();
        this.refreshed = false;
    }

    public void refresh() {
        synchronized (this.getLifecycleMonitor()) {
            this.destroy();
            this.refreshed = true;
        }
    }

    @Override
    public void destroy() {
        super.destroy();
        if (this.refreshed) {
            this.getBeanFactory().destroyScopedBean(this.getConversationId());
        }
    }
}

public class SftpBeanDefinitionRegistryPostProcessor implements BeanDefinitionRegistryPostProcessor {

    @Autowired
    private InterfaceRepository interfaceRepo;

    @Autowired
    private ConfigurableListableBeanFactory beanFactory;

    @Override
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) throws BeansException {
        // Register SessionFactoryLocator
        Map<Object, SessionFactory<LsEntry>> factories = interfaceRepo.findAll().stream()
                .map(x -> new SimpleEntry<>(new SessionFactoryKey(x.getHostname(), x.getPort(), x.getUsername()),
                        sessionFactory(x.getHostname(), x.getPort(), x.getUsername(), x.getPassword())))
                .collect(Collectors.toMap(Entry::getKey, Entry::getValue, (a, b) -> a));
        RootBeanDefinition sessionFactoryLocatorBeanDefinition = new RootBeanDefinition(DefaultSessionFactoryLocator.class);
        sessionFactoryLocatorBeanDefinition.getConstructorArgumentValues().addGenericArgumentValue(factories);
        registry.registerBeanDefinition("sessionFactoryLocator", sessionFactoryLocatorBeanDefinition);

        // Register DelegatingSessionFactory
        RootBeanDefinition delegatingSessionFactoryBeanDefinition = new RootBeanDefinition(DelegatingSessionFactory.class);
        delegatingSessionFactoryBeanDefinition.getConstructorArgumentValues().addGenericArgumentValue(beanFactory.getBean("sessionFactoryLocator"));
        registry.registerBeanDefinition("delegatingSessionFactory", delegatingSessionFactoryBeanDefinition);

        // Register RotatingServerAdvice
        List<RotationPolicy.KeyDirectory> keyDirectories = interfaceRepo.findAll().stream()
                .filter(Interface::isReceivingData)
                .map(x -> new RotationPolicy.KeyDirectory(
                        new SessionFactoryKey(x.getHostname(), x.getPort(), x.getUsername()),
                        x.getDirectory()))
                .toList();
        if (!keyDirectories.isEmpty()) {
            RootBeanDefinition rotatingServerAdviceBeanDefinition = new RootBeanDefinition(RotatingServerAdvice.class);
            rotatingServerAdviceBeanDefinition.getConstructorArgumentValues().addGenericArgumentValue(beanFactory.getBean("delegatingSessionFactory"));
            rotatingServerAdviceBeanDefinition.getConstructorArgumentValues().addGenericArgumentValue(keyDirectories);
            registry.registerBeanDefinition("rotatingServerAdvice", rotating)}
