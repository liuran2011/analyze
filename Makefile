export SB_TOP=$(shell pwd)
export BUILD_TOP=$(SB_TOP)/build

include version

all: python-analyze-deb analyze-common-deb analyze-deb report-gen-deb search-engine-deb

env: 
	@if [ ! -d $(BUILD_TOP) ]; then mkdir $(BUILD_TOP); fi

python-analyze-deb: env
	$(eval PKGNAME=$(subst -deb,,$@))
	$(eval BUILDDIR=$(BUILD_TOP)/$(PKGNAME))
	if [ ! -d $(BUILDDIR) ]; then mkdir $(BUILDDIR); fi
	cp setup.py $(BUILDDIR)
	cp -r analyze $(BUILDDIR)
	cp -r packages/$(PKGNAME)/debian $(BUILDDIR)
	sed -i 's/VERSION/$(VERSION)/' $(BUILDDIR)/debian/changelog
	cd $(BUILDDIR); fakeroot debian/rules binary

analyze-deb: env
	$(eval PKGNAME=$(subst -deb,,$@))
	$(eval BUILDDIR=$(BUILD_TOP)/$(PKGNAME))
	if [ ! -d $(BUILDDIR) ]; then mkdir $(BUILDDIR); fi
	cp -r packages/$(PKGNAME)/debian $(BUILDDIR)
	sed -i 's/VERSION/$(VERSION)/' $(BUILDDIR)/debian/changelog
	cd $(BUILDDIR); fakeroot debian/rules binary

analyze-common-deb: env
	$(eval PKGNAME=$(subst -deb,,$@))
	$(eval BUILDDIR=$(BUILD_TOP)/$(PKGNAME))
	if [ ! -d $(BUILDDIR) ]; then mkdir $(BUILDDIR); fi
	cp -r packages/$(PKGNAME)/debian $(BUILDDIR)
	sed -i 's/VERSION/$(VERSION)/' $(BUILDDIR)/debian/changelog
	cd $(BUILDDIR); fakeroot debian/rules binary

report-gen-deb: env
	$(eval PKGNAME=$(subst -deb,,$@))
	$(eval BUILDDIR=$(BUILD_TOP)/$(PKGNAME))
	if [ ! -d $(BUILDDIR) ]; then mkdir $(BUILDDIR); fi
	cp -r packages/$(PKGNAME)/debian $(BUILDDIR)
	sed -i 's/VERSION/$(VERSION)/' $(BUILDDIR)/debian/changelog
	cd $(BUILDDIR); fakeroot debian/rules binary

search-engine-deb: env
	$(eval PKGNAME=$(subst -deb,,$@))
	$(eval BUILDDIR=$(BUILD_TOP)/$(PKGNAME))
	if [ ! -d $(BUILDDIR) ]; then mkdir $(BUILDDIR); fi
	cp -r packages/$(PKGNAME)/debian $(BUILDDIR)
	sed -i 's/VERSION/$(VERSION)/' $(BUILDDIR)/debian/changelog
	cd $(BUILDDIR); fakeroot debian/rules binary



clean:
	rm -rf $(BUILD_TOP)
