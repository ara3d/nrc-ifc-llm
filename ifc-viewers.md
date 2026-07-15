Below is the broadest **verified inventory I could assemble as of July 15, 2026**. “All” cannot be guaranteed because small GitHub viewers appear and disappear frequently.

I interpret the request strictly:

* **Open-source** means the source has an identifiable open-source licence.
* **Free proprietary** viewers are listed separately.
* Pure IFC libraries and SDKs are excluded unless they include a usable viewer application or demo.
* Viewers requiring conversion from IFC to another format are marked.

## Free and open-source IFC viewers

### More mature or practically usable

| Viewer                                        | Platform                                       | IFC handling                                | Notes                                                                                                                                                                                                                                             |
| --------------------------------------------- | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **xBIM Xplorer**                              | Windows desktop; web components also available | Direct IFC                                  | Mature .NET viewer with model tree, properties, selection, visibility controls and IFCZIP/IFCXML support. ([Xbim][1])                                                                                                                             |
| **Bonsai** — formerly BlenderBIM              | Windows, macOS, Linux through Blender          | Direct/native IFC                           | Full open-source BIM authoring environment, but also one of the most capable open-source IFC viewers and inspectors. ([BonsaiBIM][2])                                                                                                             |
| **FreeCAD with NativeIFC**                    | Windows, macOS, Linux                          | Direct IFC                                  | General-purpose CAD application with IFC import and increasingly native IFC workflows. NativeIFC was integrated into FreeCAD 1.0. ([FreeCAD Wiki][3])                                                                                             |
| **F3D**                                       | Windows, macOS, Linux; web build               | Direct IFC through its WebIFC plug-in       | Lightweight, fast general-purpose 3D viewer. IFC support was added through the web-ifc integration and may depend on how the binary was packaged. ([F3D][4])                                                                                      |
| **BIMsurfer**                                 | Web                                            | IFC through BIMserver and related pipelines | One of the earliest open-source WebGL BIM viewers. Commonly deployed with BIMserver rather than as a simple local-file viewer. ([GitHub][5])                                                                                                      |
| **BIMserver**                                 | Self-hosted web/server platform                | Direct IFC ingestion                        | Open-source IFC model server with revisions, querying and geometry processing. Its visualization front end is commonly BIMsurfer. ([IFC Wiki][6])                                                                                                 |
| **IfcPlusPlus Viewer**                        | Desktop, primarily source-build                | Direct IFC                                  | MIT-licensed C++ IFC implementation with a Qt/OpenSceneGraph example viewer. More developer-oriented than polished consumer software. ([GitHub][7])                                                                                               |
| **IFClite**                                   | Web/browser                                    | Direct, client-side IFC                     | Active browser-native viewer and toolkit supporting IFC2X3, IFC4, IFC4X3 and emerging IFC5/IFCX work. MPL-2.0 licensed. A previously bundled desktop edition is no longer distributed. ([GitHub][8])                                              |
| **Bldrs Share**                               | Web; self-hostable                             | Direct IFC                                  | AGPL-licensed collaborative CAD/BIM viewer supporting IFC, STEP, STL, OBJ and glTF. ([GitHub][9])                                                                                                                                                 |
| **OpenProject BIM Edition**                   | Self-hosted web platform                       | Direct IFC upload                           | Open-source project-management platform with an integrated IFC viewer, issue management and BCF-oriented workflows. Not a standalone viewer. ([OpenProject.org][10])                                                                              |
| **xeokit-bim-viewer / xeokit-bim-viewer-app** | Web; self-hostable                             | IFC must normally be converted to XKT       | Powerful AGPL browser BIM viewer optimized for large models. Its supplied application includes an IFC-to-XKT preparation pipeline rather than directly parsing IFC in the browser. ([GitHub][11])                                                 |
| **That Open Engine / Components**             | Web                                            | Direct IFC                                  | MIT-licensed open-source BIM viewer components. The older `web-ifc-viewer` repository remains usable but is officially deprecated in favour of Components. Primarily a toolkit plus demos rather than a packaged end-user product. ([GitHub][12]) |
| **Monty IFC Viewer**                          | Windows, macOS, Linux                          | Direct IFC                                  | LGPL-licensed lightweight viewer from the OpenAEC Foundation, oriented toward construction and on-site assembly. It is young and still progressing toward broader production readiness. ([GitHub][13])                                            |
| **Microsoft IFC SDK JavaScript Viewer**       | Web/local HTML application                     | Direct IFC                                  | Apache-licensed reference viewer supplied with Microsoft’s IFC SDK. Best regarded as an experimental or developer example rather than a finished commercial-style viewer. ([GitHub][14])                                                          |

### Smaller, specialized or experimental open-source viewers

| Viewer                                | Platform                                       | Focus or limitation                                                                                                                                       |
| ------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ifc-bcf-viewer**                    | Web, single client-side application            | Direct local IFC and BCF viewing without an account or server. AGPL-3.0. ([GitHub][15])                                                                   |
| **davras5/ifc-viewer**                | Web                                            | MIT-licensed local IFC viewer with property tables, attribute colouring and spreadsheet-oriented export features. ([GitHub][16])                          |
| **IFC Classifier**                    | Web                                            | AGPL viewer aimed at inspecting and assigning classifications to IFC objects. ([GitHub][17])                                                              |
| **BIM OOTB**                          | Web                                            | MIT-licensed, local-first IFC viewer combining BIM inspection with clash, quantity and ERP-style experiments. ([GitHub][18])                              |
| **IFCFlux**                           | WebGPU/Tauri desktop technology                | Apache-2.0 experimental high-performance IFC viewer. Interesting architecture, but substantially less mature than xBIM, Bonsai or FreeCAD. ([GitHub][19]) |
| **IFC Viewer for Visual Studio Code** | VS Code extension                              | Opens IFC models inside VS Code using That Open Engine. Useful for developers rather than ordinary BIM users. ([GitHub][20])                              |
| **Uzufly Cesium IFC Viewer**          | Web/Cesium component                           | Apache-licensed experiment for placing and viewing IFC models in geospatial Cesium scenes. ([GitHub][21])                                                 |
| **ifcPipeline**                       | Self-hosted web platform                       | FastAPI-based processing platform with a That Open Components browser viewer. More of a pipeline application than a standalone viewer. ([GitHub][22])     |
| **Nomeon Shopfloor App**              | Electron desktop; Windows, macOS, Linux builds | Svelte/Electron IFC viewer aimed at fabrication or shop-floor use. ([GitHub][23])                                                                         |
| **ifc-viewer-tauri**                  | Windows, macOS, Linux when built               | Tauri desktop wrapper and template around That Open Components. Primarily useful as source code for building a custom desktop viewer. ([GitHub][24])      |

## Free but not open-source

These products are free to use, or have a permanent free viewer tier, but their complete application source is not openly licensed.

### Desktop viewers

| Viewer                         | Platform              | Notes                                                                                                                                                                                 |
| ------------------------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ODA Open IFC Viewer**        | Windows, macOS, Linux | Free cross-platform viewer from the Open Design Alliance. Opens files locally and supports recent IFC capabilities, but is proprietary. ([Open IFC Viewer][25])                       |
| **BIMcollab Zoom Viewer**      | Windows, macOS        | Free Viewer edition with IFC federation, navigation, properties, sections and issue-oriented workflows. Advanced validation and coordination require paid editions. ([BIMcollab][26]) |
| **BIMvision**                  | Windows               | Long-established freeware IFC2X3/IFC4 viewer. A broad ecosystem of optional plug-ins is available, some of which are paid. ([BIMvision][27])                                          |
| **DDScad Viewer**              | Desktop               | Free Open BIM viewer supporting IFC, BCF, DWG, gbXML, 3DS and related engineering formats. ([Graphisoft][28])                                                                         |
| **usBIM.viewer+**              | Windows               | Free IFC viewer and lightweight editor with conversion, property inspection and interoperability features. ACCA also provides a browser-based usBIM viewer. ([ACCA Software][29])     |
| **FZKViewer / KITModelViewer** | Desktop               | Free research-oriented viewer from KIT supporting IFC SPF, ifcXML, CityGML and other semantic model formats. Strong at inspecting relations and properties. ([IAI KIT][30])           |
| **Areddo**                     | Windows               | Free IFC, DWG, GML and point-cloud viewer with model-comparison and BIM inspection capabilities. ([Arkey][31])                                                                        |
| **BIM Beaver**                 | Desktop               | Free IFC2X3/IFC4 viewer with object properties and some model-editing functionality. ([BIM VILLAGE][32])                                                                              |
| **CADMATIC eBrowser Free**     | Windows               | Free design-review viewer supporting IFC and CADMATIC models, with offline navigation and review functionality. ([Cadmatic][33])                                                      |

### Browser, cloud and local-web viewers

| Viewer                          | Processing model                                   | Notes                                                                                                                                                                                                              |
| ------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Dalux BIM Viewer**            | Account/project platform                           | Free BIM viewing across browser, desktop and mobile clients. Particularly strong for field use, drawings and combined 2D/3D navigation. ([Dalux][34])                                                              |
| **Autodesk Viewer**             | Cloud upload and Autodesk account                  | Free browser viewer supporting IFC and many Autodesk/non-Autodesk formats. Files are uploaded to Autodesk’s service. ([Autodesk Viewer][35])                                                                       |
| **Trimble Connect Personal**    | Cloud account                                      | Permanent free plan with limited projects, storage and collaborators. Provides browser, Windows and mobile model viewing and coordination. ([Geospatial Solutions][36])                                            |
| **DiStellar IFC Viewer**        | Browser application                                | Free online IFC2X3/IFC4 viewer and editor. ([DiRoots][37])                                                                                                                                                         |
| **Flinker IFC Viewer**          | Local browser processing; Windows app also offered | Opens IFC locally in the browser without requiring an account or uploading the file. ([Flinker][38])                                                                                                               |
| **Sortdesk IFC Viewer**         | Local browser processing                           | Free base viewer with model tree, properties, measurements, sections and local-file processing. ([Sortdesk | Free Online IFC Viewer][39])                                                                          |
| **Swyvl IFC Viewer**            | Local browser processing                           | Free no-upload IFC viewer intended to handle comparatively large files directly in the browser. ([Swyvl][40])                                                                                                      |
| **BIMData Viewer/platform**     | Cloud and self-hosted technology                   | BIMData provides IFC viewing and collaboration services. Its viewer technology has open-source roots, but current hosted-plan limits and licensing should be checked separately. ([IFC Wiki][41])                  |
| **eveBIM**                      | Desktop/freeware                                   | French multi-scale viewer associated with CSTB, supporting IFC alongside GIS and CityGML-style data. Current distribution and maintenance status are less clear than for the major viewers above. ([IFC Wiki][42]) |
| **Constructivity Model Viewer** | Desktop/freeware                                   | IFC viewer historically listed in buildingSMART’s viewer directories; its present maintenance and availability are unclear. ([IFC Wiki][41])                                                                       |

## Discontinued or legacy free viewers

| Viewer                         | Current situation                                                                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Solibri Anywhere**           | Became a legacy product on April 13, 2026. Existing installations may continue working, but it is no longer offered to new users. ([Solibri][43]) |
| **Tekla BIMsight**             | Discontinued and replaced by Trimble Connect. ([Tekla][44])                                                                                       |
| **Solibri Model Viewer**       | Older predecessor to Solibri Anywhere; no longer the current free Solibri viewer.                                                                 |
| **That Open `web-ifc-viewer`** | Source remains available, but the project is deprecated and superseded by That Open Components. ([GitHub][12])                                    |

## Best-supported shortlist

For a practical evaluation, I would start with:

* **Open-source desktop:** xBIM Xplorer, Bonsai, FreeCAD and F3D.
* **Open-source web:** IFClite, Bldrs Share, BIMsurfer and That Open Components.
* **Free proprietary desktop:** ODA Open IFC Viewer, BIMcollab Zoom, BIMvision and FZKViewer.
* **Free no-upload browser:** Flinker, Sortdesk and Swyvl.
* **Developer foundations for a custom viewer:** That Open Components, IFClite, xeokit, xBIM and BIMsurfer/BIMserver.

[1]: https://xbim.net/xbim-xplorer/ "xBIM Xplorer - Xbim"
[2]: https://bonsaibim.org/?utm_source=chatgpt.com "Bonsai - beautiful, detailed, and data-rich OpenBIM"
[3]: https://wiki.freecad.org/Native_IFC?utm_source=chatgpt.com "Native IFC"
[4]: https://f3d.app/?utm_source=chatgpt.com "F3D: Home"
[5]: https://github.com/aothms/BIMsurfer?utm_source=chatgpt.com "aothms/BIMsurfer: The first open source WebGL based IFC ..."
[6]: https://www.ifcwiki.org/index.php/Open_Source "Open Source - IFC Wiki"
[7]: https://github.com/ifcquery/ifcplusplus?utm_source=chatgpt.com "IfcPlusPlus is an open source C++ ..."
[8]: https://github.com/LTplus-AG/ifc-lite "GitHub - LTplus-AG/ifc-lite: Parse, view, query, edit, and export IFC, IDS, BCF, pointclouds and more AEC stuff. In the browser, server or desktop. · GitHub"
[9]: https://github.com/bldrs-ai/Share?utm_source=chatgpt.com "bldrs-ai/Share"
[10]: https://www.openproject.org/docs/bim-guide/ifc-viewer/?utm_source=chatgpt.com "IFC viewer (BIM feature)"
[11]: https://github.com/xeokit/xeokit-bim-viewer?utm_source=chatgpt.com "Built with xeokit SDK. IFC, BIM and Point Cloud 3D Viewer ..."
[12]: https://github.com/ThatOpen/web-ifc-viewer?utm_source=chatgpt.com "ThatOpen/web-ifc-viewer: Graphics engine and toolkit for ..."
[13]: https://github.com/OpenAEC-Foundation/website/blob/main/index.html?utm_source=chatgpt.com "website/index.html at main · OpenAEC-Foundation ..."
[14]: https://github.com/microsoft/ifc?utm_source=chatgpt.com "GitHub - microsoft/ifc: SDK for the IFC specification at https ..."
[15]: https://github.com/arsray146/ifc-bcf-viewer/blob/main/README.md?utm_source=chatgpt.com "ifc-bcf-viewer/README.md at main"
[16]: https://github.com/davras5/ifc-viewer?utm_source=chatgpt.com "davras5/ifc-viewer"
[17]: https://github.com/louistrue/ifc-classifier?utm_source=chatgpt.com "louistrue/ifc-classifier"
[18]: https://github.com/topics/clash-detection?utm_source=chatgpt.com "clash-detection · GitHub Topics"
[19]: https://github.com/xyzbety/IFCFlux?utm_source=chatgpt.com "xyzbety/IFCFlux: Lightweight, pluggable, WebGPU-based ..."
[20]: https://github.com/chuongmep/ifc-vscode-viewer?utm_source=chatgpt.com "chuongmep/ifc-vscode-viewer"
[21]: https://github.com/uzufly/exploratory?utm_source=chatgpt.com "Uzufly Exploratory Projects"
[22]: https://github.com/jonatanjacobsson/ifcpipeline?utm_source=chatgpt.com "jonatanjacobsson/ifcpipeline: IFC Pipeline is a FastAPI- ..."
[23]: https://github.com/Nomeon/shopfloor-app?utm_source=chatgpt.com "Nomeon/shopfloor-app: IFC viewer using Electron and Svelte"
[24]: https://github.com/rrdls/ifc-viewer-tauri?utm_source=chatgpt.com "rrdls/ifc-viewer-tauri"
[25]: https://openifcviewer.com/?utm_source=chatgpt.com "Open IFC Viewer"
[26]: https://www.bimcollab.com/en/go/free-ifc-viewer/?utm_source=chatgpt.com "Download the best free IFC viewer"
[27]: https://bimvision.eu/?utm_source=chatgpt.com "BIMvision - freeware IFC model viewer"
[28]: https://www.graphisoft.com/en-ca/plans-and-products/ddscad-viewer/?utm_source=chatgpt.com "DDScad Viewer | Free Open BIM tool for everyone | Canada"
[29]: https://www.accasoftware.com/en/ifc-viewer?utm_source=chatgpt.com "IFC Viewer | usBIM - ACCA software"
[30]: https://www.iai.kit.edu/english/1648.php "KIT - IAI - Downloads - FZKViewer"
[31]: https://arkey.nl/areddo/download?utm_source=chatgpt.com "Free download: IFC viewer Areddo - Arkey Systems"
[32]: https://bim-village.net/en/bim-beaver/?utm_source=chatgpt.com "BIM BEAVER"
[33]: https://cadmatic.com/en/products/cadmatic-ebrowser/?utm_source=chatgpt.com "Cadmatic eBrowser | 3D Model Viewer for project ..."
[34]: https://www.dalux.com/en-ca/products/bim-viewer/?utm_source=chatgpt.com "World's Best BIM Viewer for Free"
[35]: https://viewer.autodesk.com/?utm_source=chatgpt.com "Autodesk Viewer | Free Online File Viewer"
[36]: https://geospatial.trimble.com/en/products/software/trimble-connect/subscription-plans?utm_source=chatgpt.com "Trimble Connect Subscription Plans"
[37]: https://diroots.com/apps/distellar/?utm_source=chatgpt.com "Free Online IFC Viewer | DiStellar Web App"
[38]: https://viewer.flinker.app/?utm_source=chatgpt.com "IFC Viewer: Free, Fast, and Private"
[39]: https://viewer.sortdesk.com/?utm_source=chatgpt.com "Sortdesk | Free Online IFC Viewer"
[40]: https://swyvl.io/tools/ifc-viewer/?utm_source=chatgpt.com "Free IFC Viewer — View BIM Models in Your Browser | Swyvl"
[41]: https://www.ifcwiki.org/index.php/Freeware "Freeware - IFC Wiki"
[42]: https://www.ifcwiki.org/index.php/Freeware?utm_source=chatgpt.com "Freeware"
[43]: https://www.solibri.com/products/solibri-anywhere?utm_source=chatgpt.com "Solibri Anywhere (Legacy) | Structured IFC Model Viewing ..."
[44]: https://www.tekla.com/products/tekla-bimsight?utm_source=chatgpt.com "Tekla BIMsight is now Trimble Connect for Windows"
